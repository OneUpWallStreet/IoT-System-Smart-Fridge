//
//  EnvironmentalDataPoint.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/4/24.
//

import Foundation

struct EnvironmentalDataPoint: Identifiable {
    let id = UUID()
    let timestamp: Date
    let humidity: Double
    let temperature: Double
}


