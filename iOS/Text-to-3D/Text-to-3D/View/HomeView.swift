//
//  HomeView.swift
//  Text-to-3D
//
//  Created by Aditya Sharma on 5/20/23.
//

import SwiftUI
import SceneKit

// ucsbece2023!
struct HomeView: View {
    @State var isToggled = true
    @State var isUnToggled = false
    @State var sliderVal: Double = 5
    var body: some View {
        VStack(spacing: 15) {
            HStack {
                Text("My Objects")
                    .font(.largeTitle.bold())
                
                Spacer(minLength: 10)
            
                Button(action: {
                    
                }) {
                    Image(systemName: "magnifyingglass")
                }
                    .foregroundColor(.black)
                    .font(.title)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(.horizontal, 15)
            
            ScrollView(.vertical, showsIndicators: false) {
                VStack(spacing: 15) {
                    ForEach(sampleData) {
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
    
    // Card View
    @ViewBuilder
    func CardView(_ model: Model) -> some View {
//        @State  isToggle = true
        GeometryReader {
            let size = $0.size
            let rect = $0.frame(in: .named("SCROLLVIEW"))
            
            let minY = rect.minY
            
            HStack(spacing: -25) {
                VStack(alignment: .leading, spacing: 6) {
                    Text("Prompt:")
                        .font(.subheadline)
                    Text(model.prompt)
                        .font(.subheadline)
                        .fontWeight(.medium)
//                        .fontWeight(.semibold)
                    
//                    Toggle("Show model", isOn: $(model.toggle))
                    if model.toggle {
                        Toggle("Show model", isOn: $isToggled)
                    } else {
                        Toggle("Show model", isOn: $isUnToggled)
                    }
                    Text("Resize")
                    Slider(value: $sliderVal, in: 0...10)
                    
                    Image(systemName: "message")
                }
                .padding(20)
                .frame(width: size.width / 2, height: size.height * 0.8)
                .background {
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(.white)
                        .shadow(color: .black.opacity(0.08), radius: 8, x: 5, y: 5)
                        .shadow(color: .black.opacity(0.08), radius: 8, x: -5, y:-5)
                }
                .zIndex(1)
                
                ZStack {
                    VStack(alignment: .leading, spacing: 10) {
                        SceneView(scene: SCNScene(named: sampleData[0].url), options: [.autoenablesDefaultLighting, .allowsCameraControl])
                    }
                    .frame(width: size.width / 2, height: size.height * 0.9)
                    .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
                    .background {
                        RoundedRectangle(cornerRadius: 10, style: .continuous)
                            .fill(.white)
                            .shadow(color: .black.opacity(0.1), radius: 5, x: 5, y: 5)
                            .shadow(color: .black.opacity(0.1), radius: 5, x: -5, y:-5)
                    }
                    //                    .aspectRatio(contentMode: .fill)
                    //                    .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
            .frame(width: size.width)
            // anchor .bottom, persepctive: 0.8
            .rotation3DEffect(.init(degrees: convertOffsetToRotation(rect)), axis: (x:1, y:0, z:0), anchor: .center, anchorZ: 1, perspective: 1)
        }
        .frame(height: 220)
    }
        
        // Convert MinY to Rotation
        func convertOffsetToRotation(_ rect: CGRect) -> CGFloat {
            let cardHeight = rect.height + 20
            let minY = rect.minY - 20
            let progress = minY < 0 ? (minY / cardHeight) : 0
            let constrainedProgress = min(-progress, 1.0)
            return constrainedProgress * 90
        }
}

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        Main()
    }
}
