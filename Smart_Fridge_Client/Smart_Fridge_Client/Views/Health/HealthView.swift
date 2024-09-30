//
//  HealthView.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/4/24.
//

import SwiftUI
import Charts


struct HealthView: View {
    
    private var dateFormatter: DateFormatter {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .short
        return formatter
    }
    
    @ObservedObject var healthVM = HealthViewModel()
    
    var body: some View {
        ScrollView {
            VStack {
                
                HStack{
                    Text("Working")
                        .bold()
                        .foregroundStyle(Color.green)
                        .font(.title)
//                        .padding()
                    Spacer()
                    Button {
                        healthVM.fetchFridgeConditions()
                    } label: {
                        Image("correct")
                            .resizable()
                            .scaledToFit()
                            .frame(width: 40, height: 40)
                    }


                }
                .padding()


                // Heading for Humidity
                HStack {
                    Text("Humidity")
                        .font(.headline)
                    Spacer()
                    Image("humidity")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 20, height: 20) 
                }
                .padding()
                
                Chart {
                    ForEach(healthVM.envData,id: \.timestamp) { point in
                        LineMark(
                            x: .value("Time", point.timestamp),
                            y: .value("Humidity (%)", point.humidity)
                        )
                        .foregroundStyle(.blue)
                        .interpolationMethod(.catmullRom)
                    }
                }
                .frame(width: 350, height: 350)
                .padding()


                HStack {
                    Text("Temperature")
                        .font(.headline) 
                    Spacer()
                    Image("temp")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 25, height: 25)
                }
                .padding()
                
                Chart {
                    ForEach(healthVM.envData,id: \.timestamp) { point in
                        LineMark(
                            x: .value("Time", point.timestamp),
                            y: .value("Temperature (°C)", point.temperature)
                        )
                        .foregroundStyle(.red)
                        .interpolationMethod(.catmullRom)
                    }
                }
                .frame(width: 350, height: 350)
                .padding()
            }
        }
    }
}
#Preview {
    HealthView()
}
