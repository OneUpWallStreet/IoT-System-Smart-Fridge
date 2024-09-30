//
//  FridgeItem.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/1/24.
//

import Foundation

struct FridgeItem: Codable {
    var account_id: String
    var item_id: String
    var classname: String
    var expiration_date: String? // Made optional to handle null
    var s3_url:String
    var expired: Bool
    var real_photo_path: String
    var timestamp: String // Corrected the typo
    
    // Initializer to create a FridgeItem from a dictionary
    init?(dictionary: [String: Any]) {
        guard let account_id = dictionary["account_id"] as? String,
              let item_id = dictionary["item_id"] as? String,
              let classname = dictionary["classname"] as? String,
              let s3_url = dictionary["s3_url"] as? String,
              let expired = dictionary["expired"] as? Bool,
              let real_photo_path = dictionary["real_photo_path"] as? String,
              let timestamp = dictionary["timestamp"] as? String else {
            return nil
        }
        
        self.account_id = account_id
        self.item_id = item_id
        self.classname = classname
        self.expiration_date = dictionary["expiration_date"] as? String // Handle optional
        self.expired = expired
        self.real_photo_path = real_photo_path
        self.timestamp = timestamp
        self.s3_url = s3_url
    }
}


