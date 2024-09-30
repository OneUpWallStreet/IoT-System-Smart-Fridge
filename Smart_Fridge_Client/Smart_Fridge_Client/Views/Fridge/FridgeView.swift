//
//  FridgeView.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/1/24.
//

import SwiftUI

struct FridgeView: View {
    
    @ObservedObject var fridgeVM = FridgeViewModel()
    @State private var showUpdateItemView = false
    @State private var selectedItem: FridgeItem?

    
    var body: some View {
        
        ScrollView{
            
            HStack{
                Text("Items")
                    .font(.title)
                    .bold()
                
                
                Spacer()
                Button {
                    fridgeVM.refresh()
                } label: {

                    HStack{
                        Image("refresh")
                            .resizable()
                            .frame(width: 25,height: 25)
                        Text("Refresh")
                            .foregroundStyle(.blue)
                        
                    }
                    
                }
            }
            .padding()

            
            
            ForEach(fridgeVM.fridgeItems, id: \.item_id) { item in
                fridgeItem(item)
                    .padding(.all)
                    .sheet(isPresented: $showUpdateItemView) {
                        UpdateItemView(item: $selectedItem) {
                            fridgeVM.refresh()
                        }
                    }

                
            }

            
        }
        
        
        
    }
    
    
    private func imageFromURL(urlString: String) -> some View {
        VStack{
            if let url = URL(string: urlString) {
                AsyncImage(url: url) { image in
                    image
                        .resizable()

                } placeholder: {
                    Image("loading")
                        .resizable()

                }
            } else {
                Image("loading")
                    .resizable()

            }
        }
    }
    
    @ViewBuilder
    private func deleteButton(_ item: FridgeItem) -> some View {
        
        Button {
            fridgeVM.deleteItem(item_id: item.item_id)
        } label: {
            Image("delete")
                .resizable()
                .frame(width: 20,height: 20)
        }
    }
    
    @ViewBuilder
    private func updateButton(_ item: FridgeItem) -> some View {
        
        Button {
            selectedItem = item
            showUpdateItemView = true
        } label: {
            Image("update")
                .resizable()
                .frame(width: 20,height: 20)
        }
        
    }
    
    
    
    
    @ViewBuilder
    private func fridgeItem(_ item: FridgeItem) -> some View {
        
        VStack {
                
            imageFromURL(urlString: item.s3_url)

            

             VStack(alignment: .leading) {
                 HStack{
                     Text(item.classname)
                         .font(.headline)
                         .foregroundColor(.black)
                    Spacer()
                 }
                 
                 HStack{
                     Text(item.expiration_date ?? "No Expiration")
                         .font(.subheadline)
                         .foregroundColor(.gray)
                     
                     if !item.expired {
                         Text("Safe To Use")
                             .font(.caption)
                             .foregroundStyle(Color.green)
                     } else{
                         Text("Not Safe To Use")
                             .font(.caption)
                             .foregroundStyle(Color.red)
                     }
                     
                     Spacer()
                     
                     
                    deleteButton(item)
                     
                    Spacer()
                     
                    updateButton(item)

                 }
                 


             }
             .padding([.leading, .bottom, .trailing])
            
         }
         .background(Color.white)
         .cornerRadius(10)
         .shadow(radius: 5)
         .padding(.horizontal)
        
    }
    
    
    
}

#Preview {
    FridgeView()
}
