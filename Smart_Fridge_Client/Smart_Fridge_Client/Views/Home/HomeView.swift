//
//  HomeView.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 2/23/24.
//

import SwiftUI
struct HomeView: View {
    
    @ObservedObject var homeVM = HomeViewModel()
    
    var body: some View {
        
        VStack {
            
            tempAndHumView
            
            Spacer()

            Button {
                homeVM.fetchFridgePhoto()
                homeVM.fetchTempHumidity()
            } label: {
                if homeVM.fridgePhotoURL != nil {
    //                imageFromURL(urlString: "https://as2.ftcdn.net/v2/jpg/04/75/00/01/1000_F_475000168_bjvpSfEcsDJKWZkvfkZLBMgExmerFWl7.jpg")
                    imageFromURL(urlString: homeVM.fridgePhotoURL!)
                }
                else{
                    imageFromURL(urlString: "https://t4.ftcdn.net/jpg/03/16/15/47/360_F_316154790_pnHGQkERUumMbzAjkgQuRvDgzjAHkFaQ.jpg")
                }
            }


            
            Spacer()
        }
        .background(Color.white)
        .onAppear {
            homeVM.fetchFridgePhoto()
        }
    }
    
    private func imageFromURL(urlString: String) -> some View {
        VStack{
            if let url = URL(string: urlString) {
                AsyncImage(url: url) { image in
                    image
                        .resizable()
                        .frame(width: 350,height: 400)
                        .clipShape(RoundedRectangle(cornerRadius: 25.0))
                } placeholder: {
                    Image("loading")
                        .resizable()
                        .frame(width: 350,height: 400)
                        .clipShape(RoundedRectangle(cornerRadius: 25.0))
                }
            } else {
                Image("milk")
                    .resizable()

            }
        }
    }
    
    var tempAndHumView: some View {
        
        VStack {
            
            HStack {
                Text("Hello Swarom 👋🏻")
                    .font(.title)
                    .fontWeight(.semibold)
                    .foregroundColor(Color.primary)
                
                Spacer()
                
                // Assuming you have an Image named "fridge_icon" in your assets
                Image("fridge_icon")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 50, height: 50)
            }
            .padding()

            HStack {
                
                Spacer()
                
                ConditionDisplayView(value: homeVM.temp, title: "Temperature", color: .blue)
                
                Spacer()
                
                ConditionDisplayView(value: homeVM.hum, title: "Humidity", color: .red)
                
                Spacer()
            }
            .padding(.horizontal)
        }
    }
    
    struct ConditionDisplayView: View {
        var value: String
        var title: String
        var color: Color
        
        var body: some View {
            VStack {
                Text("\(value)°")
                    .font(.largeTitle)
                    .fontWeight(.heavy)
                    .foregroundColor(.white)
                    .frame(width: 120, height: 120)
                    .background(color)
                    .clipShape(RoundedRectangle(cornerRadius: 20))
                
                Text(title)
                    .font(.headline)
                    .foregroundColor(.primary)
            }
            .padding()
        }
    }
}


#Preview {
    HomeView()
}
