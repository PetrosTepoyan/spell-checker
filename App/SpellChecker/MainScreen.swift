//
//  MainScreen.swift
//  SpellChecker
//
//  Created by Petros Tepoyan on 14.05.2023.
//

import SwiftUI

struct MainScreen: View {
    
    @ObservedObject var viewModel: MainScreenViewModel = MainScreenViewModel()
    
    @FocusState var isFocused: Bool
    
    private let correctionsSectionHeight: CGFloat = 100
    
    var body: some View {
        VStack {
            
            Group {
                if !viewModel.corrections.isEmpty {
                    VStack(spacing: 15) {
                        
                        Text("Corrections")
                            .font(.system(size: 22, weight: .medium, design: .monospaced))
                        
                        HStack {
                            ForEach(viewModel.corrections, id: \.self) { corr in
                                Text(corr)
                                    .font(.system(size: 20, weight: .medium, design: .monospaced))
                                    .foregroundColor(.white)
                                    .padding(5)
                                    .padding(.horizontal, 5)
                                    .background(
                                        Capsule(style: .continuous)
                                            .fill(Color.gray)
                                    )
                                    .onTapGesture {
                                        withAnimation(.spring()) {
                                            var split: [String] = viewModel.text.split(separator: " ").map({ String($0) })
                                            split[split.count - 1] = corr
                                            viewModel.text = split.joined(separator: " ")
                                            viewModel.corrections.removeAll()
                                        }
                                    }
                            }
                        }
                    }
                }
            }
            .contentShape(Rectangle())
            .frame(height: correctionsSectionHeight)
            .animation(.spring(), value: viewModel.corrections)
            
            
            TextField("Your text...", text: $viewModel.text)
                .keyboardType(.default)
                .autocorrectionDisabled()
                .padding(.leading, 10)
                .focused($isFocused)
                .font(.system(size: 22, weight: .medium, design: .monospaced))
                .padding()
                .background(
                    Capsule(style: .continuous)
                        .fill(Color.white)
                        .shadow(color: .gray.opacity(isFocused ? 0.8 : 0.5), radius: isFocused ? 6 : 4)
                        .animation(.spring(), value: isFocused)
                )
                .background(
                    Capsule(style: .continuous)
                        .stroke(isFocused ? Color.blue : Color.gray, lineWidth: isFocused ? 4 : 2)
                        .animation(.spring(), value: isFocused)
                )
                .padding()
            
        }
        .frame(alignment: .center)
        .contentShape(Rectangle())
        .offset(y: -(viewModel.corrections.isEmpty ? 0 : correctionsSectionHeight))
        .onTapGesture {
            isFocused = false
        }
        
    }
}

struct MainScreen_Previews: PreviewProvider {
    static var previews: some View {
        MainScreen()
    }
}
