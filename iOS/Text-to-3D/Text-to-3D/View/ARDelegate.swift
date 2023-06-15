//
//  ARDelegate.swift
//  Text-to-3D
//
//  Created by Aditya Sharma on 5/20/23.
//

import Foundation
import ARKit
import UIKit

class ARDelegate: NSObject, ARSCNViewDelegate, ObservableObject {
    private var arView: ARSCNView?

    func setARView(_ arView: ARSCNView) {
        self.arView = arView
        
        let configuration = ARWorldTrackingConfiguration()
        configuration.planeDetection = .horizontal
        arView.session.run(configuration)
        
        arView.delegate = self
        arView.scene = SCNScene(named: "dog.obj")!
    }
    
    
}
