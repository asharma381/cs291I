//
//  Notebook.swift
//  ARKitDemo
//
//  Created by Aditya Sharma on 4/10/23.
//

import ARKit

class Notebook: SCNNode {
    func loadModel(path: URL) {
//    func loadModel() {
//        guard let virtualObject = SCNScene(named: "example_mesh_0.obj") else {return}
        
        guard let virtualObject = try? SCNScene(url: path) else {return}
        // OLD WORKING VERSION
//        guard let virtualObject = SCNScene(named: "example_mesh_0.obj") else {return}

//        guard let virtualObject = SCNScene(named: "blender.dae") else {return}
        
//        virtualObject.rootNode.childNodes.first?.scale = SCNVector3(0.1, 0.1, 0.1)
//        print(virtualObject.rootNode.childNodes.)
//        virtualObject.accessibilityFrame.size
        
        print("loaded: ", virtualObject )
        
        let wrapperNode = SCNNode()
        
        for child in virtualObject.rootNode.childNodes {
            wrapperNode.addChildNode(child)
        }
        self.addChildNode(wrapperNode)
        
        
    }
}
