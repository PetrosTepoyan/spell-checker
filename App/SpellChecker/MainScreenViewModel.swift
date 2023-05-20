//
//  MainScreenViewModel.swift
//  SpellChecker
//
//  Created by Petros Tepoyan on 14.05.2023.
//

import SwiftUI
import Combine
import Foundation

final class MainScreenViewModel: ObservableObject {
    
    @Published var text: String = ""
    
    @Published var corrections: [String] = []
    
    private var bag: Set<AnyCancellable> = []
    
    var lastWord: String {
        String(text.split(separator: " ").last ?? "")
    }
    
    init() {
        self.$text
            .debounce(for: .milliseconds(1000), scheduler: RunLoop.main)
            .filter({ !$0.isEmpty })
            .sink { newValue in
                NetworkService.shared.requestCorrections(for: newValue) { result in
                    switch result {
                    case .success(let corrections):
                        if !corrections.joined().contains(self.lastWord) {
                            withAnimation(.spring()) {
                                self.corrections = corrections
                            }
                        }
                    case .failure(let failure):
                        print(failure)
                    }
                }
            }
            .store(in: &bag)
        
        self.$text
            .sink { _ in
                withAnimation(.spring()) {
                    self.corrections.removeAll()
                }
            }
            .store(in: &bag)
    }
}
