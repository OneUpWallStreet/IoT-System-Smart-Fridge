//
//  HealthViewModel.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/4/24.
//

import Foundation


class HealthViewModel: ObservableObject {
    
    
//    func fetchFridgePhoto() {
//        GeneralRequestManager.sharedInstance.getCurrentFridgePhoto { [weak self] fridgePhotoResponse in
//            DispatchQueue.main.async {
//                if fridgePhotoResponse != nil {
//                    self?.fridgePhotoURL = fridgePhotoResponse!.url
//                }
//            }
//        }
//    }
    
    func fetchFridgeConditions() {
        GeneralRequestManager.sharedInstance.fetchFridgeConditions { [weak self] conditions in
            DispatchQueue.main.async {
                print("Updated")
                self?.envData = conditions
            }
        }
    }
    
    init() {
//        envData = PlaceholderData.sharedInstance.get_temp_humidity()
        fetchFridgeConditions()
    }
    
    @Published var envData: Array<FridgeConditions> = []
    
}
