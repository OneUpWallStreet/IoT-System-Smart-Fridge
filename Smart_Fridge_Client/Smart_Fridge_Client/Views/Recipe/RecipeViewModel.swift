//
//  RecipeViewModel.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/12/24.
//

import Foundation



class RecipeViewModel: ObservableObject {
    
    
    @Published var recipe: String?

    
    
    func getRecipe() {
        GeneralRequestManager.sharedInstance.getCurrentRecipe {  [weak self] newRecipe in
            DispatchQueue.main.async {
                self?.recipe = newRecipe
            }
        }
    }
    
    
}
