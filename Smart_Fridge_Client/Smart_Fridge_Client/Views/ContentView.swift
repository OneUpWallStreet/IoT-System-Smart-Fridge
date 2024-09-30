//
//  ContentView.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 2/23/24.
//

import SwiftUI

struct ContentView: View {
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
                .tag(0)

            HealthView()
                .tabItem {
                    Label("Health", systemImage: "heart.fill")
                }
                .tag(1)
            
            RecipeView()
                .tabItem {
                    Label("Recipe", systemImage: "cart.fill")
                }
                .tag(2)
            
            FridgeView()
                .tabItem {
                    Label("Fridge", systemImage: "ev.charger.fill")
                }
                .tag(3)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
