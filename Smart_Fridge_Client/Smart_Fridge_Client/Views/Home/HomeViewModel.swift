//
//  HomeViewController.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 2/23/24.
//

import Foundation



class HomeViewModel: ObservableObject {
    
    @Published var fridgePhotoURL: String?
    @Published var temp: String = "0.0"
    @Published var hum: String = "0.0"
    
    func fetchFridgePhoto() {
        GeneralRequestManager.sharedInstance.getCurrentFridgePhoto { [weak self] fridgePhotoResponse in
            DispatchQueue.main.async {
                if fridgePhotoResponse != nil {
                    self?.fridgePhotoURL = fridgePhotoResponse!.url
                }
            }
        }
    }
    
    func fetchTempHumidity() {
        GeneralRequestManager.sharedInstance.fetchCurrentFridgeConditions {  [weak self] conditions in
            DispatchQueue.main.async {
                if conditions != nil {
                    self?.temp = conditions!.temperature
                    self?.hum = conditions!.humidity
                }
            }
        }
    }
    
    init() {
        fetchFridgePhoto()
        fetchTempHumidity()
    }
}
