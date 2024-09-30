//
//  GeneralRequestManager.swift
//  Smart_Fridge_Client
//
//  Created by Arteezy on 3/11/24.
//

import Foundation





class GeneralRequestManager {
    
    static let sharedInstance = GeneralRequestManager()
    
    func fetchCurrentFridgeConditions(completion: @escaping (FridgeConditions?) -> Void) {
        guard let url = URL(string: ServerURLs.conditions.rawValue) else {
            print("Invalid URL")
            completion(nil)
            return
        }
        
        var request = URLRequest(url: url)
        
        // Add the necessary headers to your request
        request.addValue("YourCameraAPIKey", forHTTPHeaderField: "X-API-KEY")
        request.addValue("MOBILE", forHTTPHeaderField: "DEVICE")
        
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            // Check for errors or no data
            if let error = error {
                print("Error fetching data: \(error)")
                completion(nil)
                return
            }
            
            guard let data = data else {
                print("Did not receive data")
                completion(nil)
                return
            }
            
            // Attempt to decode the data into an array of FridgeConditions
            do {
                let decoder = JSONDecoder()
                let fridgeConditions = try decoder.decode([FridgeConditions].self, from: data)
                completion(fridgeConditions[0])
            } catch {
                completion(nil)
                print("Error decoding data: \(error)")
            }
        }
        
        // Start the network request
        task.resume()
    }


    func deleteItem(itemID: String) {
        
        guard let url = URL(string: "http://52.52.9.39:5000/item/\(itemID)") else {
            print("Invalid URL")
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "DELETE"

        // Set the request headers
        request.addValue("YourCameraAPIKey", forHTTPHeaderField: "X-API-KEY")
        request.addValue("MOBILE", forHTTPHeaderField: "DEVICE")

        let session = URLSession.shared
        let task = session.dataTask(with: request) { data, response, error in
            // Handle the error scenario
            if let error = error {
                print("Error: \(error.localizedDescription)")
                return
            }
            
            // Ensure you get a valid response
            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                print("Error: Invalid response or status code")
                return
            }
            
            // Parse the JSON data
            if let data = data {
                do {
                    if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
                       let message = json["message"] as? String {
                        print(message) // "Item deleted successfully"
                    }
                } catch {
                    print("JSON error: \(error.localizedDescription)")
                }
            }
        }

        // Perform the request
        task.resume()
    }
    
    
    func fetchFridgeConditions(completion: @escaping ([FridgeConditions]) -> Void) {
        // Specify the URL
        guard let url = URL(string: "http://52.52.9.39:5000/fridge/conditions/historical") else {
            print("Invalid URL")
            completion([])
            return
        }
        
        // Create a URLRequest object
        var request = URLRequest(url: url)
        // Add the necessary headers
        request.addValue("YourCameraAPIKey", forHTTPHeaderField: "X-API-KEY")
        request.addValue("MOBILE", forHTTPHeaderField: "DEVICE")
        request.httpMethod = "GET" // Specify the request method
        
        // Create a URLSessionDataTask to fetch the data
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            // Check for errors
            if let error = error {
                print("Error fetching data: \(error)")
                return
            }
            
            // Ensure there is data to decode
            guard let data = data else {
                print("No data received")
                completion([])
                return
            }
            
            // Attempt to decode the JSON response
            do {
                let decoder = JSONDecoder()
                let fridgeConditions = try decoder.decode([FridgeConditions].self, from: data)
                completion(fridgeConditions)
                // Process the fetched conditions (example: print them)
//                for condition in fridgeConditions {
//                    print("Timestamp: \(condition.timestamp), Temperature: \(condition.temperature), Humidity: \(condition.humidity)")
//                }
            } catch {
                completion([])
                print("Error decoding data: \(error)")
            }
        }
        
        // Start the task
        task.resume()
    }

    
    
    func updateItem(item: FridgeItem, newClassName: String, newExpirationDate: String, newExpired: Bool) {
        // Define the URL for the request
        if let url = URL(string: ServerURLs.updateItem.rawValue) {
            // Prepare the request
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            
            // Set the request headers
            request.addValue("YourCameraAPIKey", forHTTPHeaderField: "X-API-KEY")
            request.addValue("MOBILE", forHTTPHeaderField: "DEVICE")
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")
            
            // Prepare the JSON data to be sent with the request
            let jsonData = [
                "account_id": item.account_id,
                "classname": newClassName,
                "expiration_date": newExpirationDate,
                "expired": newExpired,
                "item_id": item.item_id,
                "real_photo_path": item.real_photo_path,
                "timestamp": item.timestamp
            ] as [String: Any]
            
            do {
                request.httpBody = try JSONSerialization.data(withJSONObject: jsonData, options: [])
            } catch let error {
                print("Error serializing JSON: \(error)")
                return
            }
            
            // Send the request
            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                // Handle errors
                if let error = error {
                    print("Error making request: \(error)")
                    return
                }
                
                // Parse the response
                guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
                    print("Server error")
                    return
                }
                
                if let mimeType = httpResponse.mimeType, mimeType == "application/json", let data = data {
                    do {
                        // Parse the JSON response
                        if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
                           let message = json["message"] as? String {
                            print(message) // "Item updated successfully"
                        }
                    } catch {
                        print("JSON Error: \(error)")
                    }
                }
            }
            
            task.resume()
        }

    }
    
//    func updateItem(item: FridgeItem) {
//        let urlString = "http://52.52.9.39:5000/item/update" // Use your server URL here
//        guard let url = URL(string: urlString) else {
//            print("Invalid URL")
//            return
//        }
//        
//        var request = URLRequest(url: url)
//        request.httpMethod = "POST"
//        request.addValue("YourCameraAPIKey", forHTTPHeaderField: "X-API-KEY")
//        request.addValue("MOBILE", forHTTPHeaderField: "DEVICE")
//
//        // Serialize your FridgeItem to JSON
//        let encoder = JSONEncoder()
//        encoder.dateEncodingStrategy = .iso8601 // If your date strings are in ISO8601 format
//        
//        var itemDictionary: [String: Any] = [
//            "account_id": item.account_id,
//            "item_id": item.item_id,
//            "classname": item.classname,
//            "expired": item.expired,
//            "real_photo_path": item.real_photo_path,
//            "timestamp": item.timestamp,
//            "expiration_date": "something"
//        ]
//        
//        // Optionally adding "expiration_date"
////        if let expirationDate = item.expiration_date {
////            itemDictionary["expiration_date"] = expirationDate
////
//        
//        do {
//            let jsonData = try JSONSerialization.data(withJSONObject: itemDictionary, options: [])
//            request.httpBody = jsonData
//            print("Request Body: \(String(data: jsonData, encoding: .utf8) ?? "Unable to print request body")")
//            
//            let session = URLSession.shared
//            
//            let task = session.dataTask(with: request) { data, response, error in
//                guard let data = data, error == nil else {
//                    print("Error here: \(error?.localizedDescription ?? "Unknown error")")
//                    return
//                }
//                
//                if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 {
//                    // Check the response
//                    do {
//                        if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any], let message = json["message"] as? String {
//                            print(message) // Should print "Item updated successfully"
//                        }
//                    } catch {
//                        print("Error parsing response data")
//                    }
//                } else {
//                    if let httpResponse = response as? HTTPURLResponse {
//                        print("Server responded with status code: \(httpResponse.statusCode)")
//                    } else {
//                        print("Invalid server response")
//                    }
//                }
//            }
//            task.resume()
//            
//        } catch {
//            print("Error serializing JSON: \(error.localizedDescription)")
//        }
//    }
    

    func getCurrentRecipe(completion: @escaping (String?) -> Void) {
                
        let urlString = ServerURLs.recipe.rawValue
        guard let url = URL(string: urlString) else {
            print("Invalid URL")
            completion(nil) // Return nil if the URL is invalid
            return
        }

        var request = generateRequestWithHeader(url)


        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                print("Network request failed: \(error?.localizedDescription ?? "No error description")")
                completion(nil) // Return nil in case of network request failure
                return
            }

            do {
                let decoder = JSONDecoder()
                let recipeResponse = try decoder.decode(RecipeResponse.self, from: data)
                DispatchQueue.main.async {
                    completion(recipeResponse.recipe) // Return the decoded response
                }
            } catch {
                print("getCurrentRecipe: Failed to decode JSON: \(error.localizedDescription)")
                completion(nil) // Return nil if decoding fails
            }
        }

        task.resume()
        
        
    }
    
    
    private func generateRequestWithHeader(_ url: URL) -> URLRequest{
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.addValue("YourCameraAPIKey", forHTTPHeaderField: "X-API-KEY")
        request.addValue("MOBILE", forHTTPHeaderField: "DEVICE")
        return request
    }
    
    
    
    
    func getCurrentFridgePhoto(completion: @escaping (FridgePhotoResponse?) -> Void) {
        
        
        let urlString = ServerURLs.currentFridgePhoto.rawValue
        
        guard let url = URL(string: urlString) else {
            print("Invalid URL")
            completion(nil) // Return nil if the URL is invalid
            return
        }
        
        
        var request = generateRequestWithHeader(url)


        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            guard let data = data, error == nil else {
                
                print("Current Fridge Photo: Network request failed: \(error?.localizedDescription ?? "No error description")")
                completion(nil) // Return nil in case of network request failure
                return
            }
            let jsonString = String(data: data, encoding: .utf8)
//            print("Current Fridge Photo: Received JSON string: \(jsonString ?? "nil")")
            do {
                let decoder = JSONDecoder()
                let fridgePhotoResponse = try decoder.decode(FridgePhotoResponse.self, from: data)
                DispatchQueue.main.async {
                    completion(fridgePhotoResponse) // Return the decoded response
                }
            } catch {
                print("Current Fridge Photo: Failed to decode JSON: \(error.localizedDescription)")
                completion(nil) // Return nil if decoding fails
            }
        }

        task.resume()
    }
    
//    func getItemPhoto(fridgeItemID: String, completion: @escaping (ItemPhotoResponse?) -> Void) {
//        
//        let urlString = "http://52.52.9.39:5000/mobile/recipe"
//        guard let url = URL(string: urlString) else {
//            print("Invalid URL")
//            completion(nil)
//            return
//        }
//
//        var request = generateRequestWithHeader(url)
//
//                
//        let task = URLSession.shared.dataTask(with: request) { data, response, error in
//            guard let data = data, error == nil else {
//                print("Network request failed: \(error?.localizedDescription ?? "Unknown error")")
//                completion(nil)
//                return
//            }
//            let jsonString = String(data: data, encoding: .utf8)
//            print("Received JSON string: \(jsonString ?? "nil")")
//
//            do {
//                let decoder = JSONDecoder()
//                let photoResponse = try decoder.decode(ItemPhotoResponse.self, from: data)
//                DispatchQueue.main.async {
//                    completion(photoResponse)
//                }
//            } catch {
//                print("getItemPhoto Failed to decode JSON: \(error.localizedDescription)")
//                completion(nil)
//            }
//        }
//
//        task.resume()
//    }

    // Assuming FridgeItem struct is defined somewhere in your code

    func getFridgeItems(completion: @escaping ([FridgeItem]) -> Void) {

//        let urlString = "http://52.52.9.39:5000/fridge/items"
        let urlString = ServerURLs.getItems.rawValue
        
        guard let url = URL(string: urlString) else {
            print("Invalid URL")
            completion([]) // Return an empty array in case of invalid URL
            return
        }

        var request = generateRequestWithHeader(url)

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error)")
                completion([]) // Return an empty array in case of error
                return
            }
            
            guard let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) else {
                print("Server Error")
                completion([]) // Return an empty array in case of server error
                return
            }
            
            guard let mimeType = httpResponse.mimeType, mimeType == "application/json",
                  let data = data else {
                print("Wrong MIME type or no data")
                completion([]) // Return an empty array in case of wrong MIME type or no data
                return
            }
            
            let jsonString = String(data: data, encoding: .utf8)
//            print("Received JSON string: \(jsonString ?? "nil")")

            
            do {
                if let jsonArray = try JSONSerialization.jsonObject(with: data) as? [[String: Any]] {
                    let fridgeItems = jsonArray.compactMap { FridgeItem(dictionary: $0) }
                    completion(fridgeItems) // Return the array of FridgeItem structs
                } else {
                    print("Invalid JSON format")
                    completion([]) // Return an empty array in case of invalid JSON format
                }
            } catch {
                print("JSON error: \(error.localizedDescription)")
                completion([]) // Return an empty array in case of JSON error
            }
        }

        task.resume()
    }

}
