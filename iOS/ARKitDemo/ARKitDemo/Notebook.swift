//
//  Notebook.swift
//  ARKitDemo
//
//  Created by Aditya Sharma on 4/10/23.
//

import ARKit

class Notebook: SCNNode {
    func loadModel(path: URL) {
//        guard let virtualObject = SCNScene(named: "eg.obj") else {return}
        
        guard let virtualObject = try? SCNScene(url: path) else {return}
        // OLD WORKING VERSION
//        guard let virtualObject = SCNScene(named: "example_mesh_0.obj") else {return}

//        guard let virtualObject = SCNScene(named: "blender.dae") else {return}
        
        print("loaded: ", virtualObject )
        
        let wrapperNode = SCNNode()
        
        for child in virtualObject.rootNode.childNodes {
            wrapperNode.addChildNode(child)
        }
        self.addChildNode(wrapperNode)
        
        
    }
}
