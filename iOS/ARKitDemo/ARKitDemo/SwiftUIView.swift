//
//  SwiftUIView.swift
//  Pods
//
//  Created by Aditya Sharma on 5/17/23.
//

import SwiftUI
import SceneKit

struct SwiftUIView: View {
    var path: URL!
    var prompt: String!
    
    init(path: URL, prompt: String) {
        self.path = path
        self.prompt = prompt
        print("SWIFT UI VIEW PATH")
        print(path)
        if !data.contains(Model(prompt: self.prompt, url: self.path)){
            data.append(.init(prompt: self.prompt, url: self.path))
        }
    }
    
    var body: some View {
        VStack(spacing: 25) {
            HStack {
                Text("My Objects")
                    .font(.largeTitle.bold())
                
                Spacer(minLength: 10)
            
                Button(action: {
                    
                }) {
                    // magnifyingglass
                    Image(systemName: "rotate.3d")
                }
                    .foregroundColor(.black)
                    .font(.title)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.horizontal, 15)
            
            ScrollView(.vertical, showsIndicators: false) {
                VStack(spacing: 15) {
                    ForEach(data) {
                        CardView($0) // $0 = sampleData[i]
                    }
                }
                .padding(.horizontal, 15)
                .padding(.vertical)
            }
            .coordinateSpace(name: "SCROLLVIEW")
            .padding(.top, 15)
        }
    }
    
    
    @ViewBuilder
    func CardView(_ model: Model) -> some View {
        GeometryReader {
            let rect = $0.frame(in: .named("SCROLLVIEW"))
            
            HStack(spacing: -25) {
                VStack(alignment: .leading, spacing: 6) {
                    Text("Prompt: " + model.prompt)
                        .font(.subheadline)
                        .fontWeight(.semibold)
//                    Image(systemName: "message")
                }
                .padding(20)
                .background {
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(.white)
                        .shadow(color: .black.opacity(0.08), radius: 8, x: 5, y: 5)
                        .shadow(color: .black.opacity(0.08), radius: 8, x: -5, y:-5)
                }
                .zIndex(1)
                
                ZStack {
                    VStack(alignment: .leading, spacing: 10) {
//                        guard let virtualObject = try? SCNScene(url: data[0].url) else {}
                        SceneView(scene: try? SCNScene(url: model.url), options: [.autoenablesDefaultLighting, .allowsCameraControl])
                    }
                    .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
                    .background {
                        RoundedRectangle(cornerRadius: 10, style: .continuous)
                            .fill(.white)
                            .shadow(color: .black.opacity(0.1), radius: 5, x: 5, y: 5)
                            .shadow(color: .black.opacity(0.1), radius: 5, x: -5, y:-5)
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
        .frame(height: 220)
    }
}

struct SwiftUIView_Previews: PreviewProvider {
    static var previews: some View {
        SwiftUIView(path: URL(string: "")!, prompt: "a dog")
    }
}
