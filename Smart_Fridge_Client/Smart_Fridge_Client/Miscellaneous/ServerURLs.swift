//
//  ServerURLs.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/12/24.
//

import Foundation


enum ServerURLs: String {
    
    case conditions = "http://52.52.9.39:5000/fridge/conditions"
    case getItems = "http://52.52.9.39:5000/fridge/items"
    case recipe  = "http://52.52.9.39:5000/mobile/recipe"
    case currentFridgePhoto = "http://52.52.9.39:5000/fridge/photo"
    case updateItem = "http://52.52.9.39:5000/item/update"
}
