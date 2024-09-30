//
//  PlaceholderData.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/1/24.
//

import Foundation


class PlaceholderData {
    
    static let sharedInstance = PlaceholderData()
    
//    Placeholder for
//    /fridge/items
    func get_fridge_items() -> Array<FridgeItem> {
        return []
    }
    
    func get_temp_humidity() -> [EnvironmentalDataPoint] {
        let environmentalData: [EnvironmentalDataPoint] = [
            EnvironmentalDataPoint(timestamp: Date(), humidity: 50.1, temperature: 20.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(1000), humidity: 45.1, temperature: 25.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(2000), humidity: 40.1, temperature: 22.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(3000), humidity: 47.1, temperature: 24.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(4000), humidity: 52.1, temperature: 17.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(5000), humidity: 55.2, temperature: 19.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(6000), humidity: 43.8, temperature: 21.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(7000), humidity: 46.5, temperature: 23.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(8000), humidity: 48.3, temperature: 18.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(9000), humidity: 49.7, temperature: 20.5),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(10000), humidity: 51.0, temperature: 22.5),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(11000), humidity: 53.2, temperature: 24.5),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(12000), humidity: 50.4, temperature: 21.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(13000), humidity: 48.9, temperature: 23.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(14000), humidity: 47.3, temperature: 25.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(15000), humidity: 49.5, temperature: 19.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(16000), humidity: 50.7, temperature: 21.5),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(17000), humidity: 52.4, temperature: 20.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(18000), humidity: 54.1, temperature: 22.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(19000), humidity: 55.5, temperature: 24.0),
            EnvironmentalDataPoint(timestamp: Date().addingTimeInterval(20000), humidity: 53.9, temperature: 23.5),
        ]
        return environmentalData
    }
    
    
}
