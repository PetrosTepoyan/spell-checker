//
//  NetworkService.swift
//  SpellChecker
//
//  Created by Petros Tepoyan on 18.05.2023.
//

import Foundation

class NetworkService {
    
    let endpoint: String = "http://127.0.0.1:8000/correction/"
    
    static let shared: NetworkService = NetworkService()
    
    init() {}
    
    func requestCorrections(for string: String, completion: @escaping (Result<[String], Error>) -> ()) {
        
        let url = URL(string: endpoint + string.split(separator: " ").joined(separator: "_"))!
        
        print("Requesting", url)
        
        var urlRequest = URLRequest(url: url)
        urlRequest.httpMethod = "GET"
        
        URLSession.shared.dataTask(with: urlRequest) { data, response, error in
            if let error {
                completion(.failure(error))
            }
            
            if let data, let values = try? JSONDecoder().decode([String].self, from: data) {
                completion(.success(values))
            } else {
                completion(.failure(NetworkError.decode))
            }
        }.resume()
    }
    
    enum NetworkError: Error {
        case decode
    }
}
