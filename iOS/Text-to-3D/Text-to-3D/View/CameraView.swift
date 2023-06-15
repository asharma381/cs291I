//
//  CameraView.swift
//  Text-to-3D
//
//  Created by Aditya Sharma on 5/20/23.
//

import SwiftUI
//import SceneKit
import ARKit

struct CameraView: View {
    @ObservedObject var arDelegate = ARDelegate()
    
    var body: some View {
        ARViewRepresentable(arDelegate: arDelegate)
            .ignoresSafeArea()
    }
}

struct CameraView_Previews: PreviewProvider {
    static var previews: some View {
        CameraView()
    }
}
