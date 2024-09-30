//
//  FridgeConditions.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/12/24.
//

import Foundation
//
//[
//    {
//        "account_id": "XXXXXX",
//        "humidity": "37.4",
//        "temperature": "75.02",
//        "timestamp": "2024-03-12T15:11:59.534370"
//    }
//]

struct FridgeConditions: Decodable {
    var account_id: String
    var humidity: String
    var temperature: String
    var timestamp: String
}
