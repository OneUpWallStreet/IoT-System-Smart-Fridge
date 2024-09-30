//
//  UpdateItemView.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/13/24.
//

import SwiftUI

struct UpdateItemView: View {
    @Binding var item: FridgeItem?
    @State private var updatedClassname: String = ""
    @State private var nonOptionalExpirationDate: Date = Date() // New non-optional Date state
    @State private var updatedExpired: Bool = false
    @Environment(\.presentationMode) var presentationMode
    var onItemUpdated: (() -> Void)?
    
    private func updateItem(item: FridgeItem){
        GeneralRequestManager.sharedInstance.updateItem(item: item, newClassName: updatedClassname, newExpirationDate: DateFormatter.yyyyMMdd.string(from: nonOptionalExpirationDate), newExpired: updatedExpired)
    }

    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Update Item")) {
                    TextField("Item Name", text: $updatedClassname)
                        .onAppear {
                            updatedClassname = item?.classname ?? ""
                        }
                    
                    DatePicker("Expiration Date", selection: $nonOptionalExpirationDate, displayedComponents: .date)
                        .onAppear {
                            if let expirationDate = item?.expiration_date {
                                nonOptionalExpirationDate = DateFormatter.yyyyMMdd.date(from: expirationDate) ?? Date()
                            }
                        }
                    
                    Toggle("Expired", isOn: $updatedExpired)
                        .onAppear {
                            updatedExpired = item?.expired ?? false
                        }
                }
            }
            .navigationBarTitle("Update Item")
            .navigationBarItems(trailing: updateButton)
        }
    }
    
    private var updateButton: some View {
        Button("Update") {
            if var item = item {
                item.classname = updatedClassname
                item.expiration_date = DateFormatter.yyyyMMdd.string(from: nonOptionalExpirationDate)
                item.expired = updatedExpired
            }
            if item != nil {
                updateItem(item: item!)
            }
            presentationMode.wrappedValue.dismiss()
            onItemUpdated?()
        }
    }
}

// Helper extension for date formatting
extension DateFormatter {
    static let yyyyMMdd: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter
    }()
}
//#Preview {
////    UpdateItemView()
//}
