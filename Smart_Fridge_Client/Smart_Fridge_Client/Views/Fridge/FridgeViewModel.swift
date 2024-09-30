//
//  FridgeViewController.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/1/24.
//

import Foundation
import Combine


class FridgeViewModel: ObservableObject {
    
    @Published var fridgeItems: [FridgeItem] = []

    init() {
        fetchFridgeItems()
    }
    
    func refresh() {
        fridgeItems = []
        fetchFridgeItems()
    }

    
    func fetchFridgeItems() {
        GeneralRequestManager.sharedInstance.getFridgeItems { [weak self] items in
            DispatchQueue.main.async {
                self?.fridgeItems = items
            }
            
        }
    }
    
    func updateItem(item_id: String) {
        print("Updating Item: \(item_id)")
    }
    
    func deleteItem(item_id: String) {
        
//        print("Delete Item with id: \(item_id)")
        GeneralRequestManager.sharedInstance.deleteItem(itemID: item_id)
        refresh()
    }
}
