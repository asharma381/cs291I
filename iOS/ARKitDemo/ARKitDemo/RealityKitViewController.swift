//
//  RealityKitViewController.swift
//  ARKitDemo
//
//  Created by Aditya Sharma on 5/26/23.
//

import UIKit
import RealityKit
import ARKit

class RealityKitViewController: UIViewController {

    @IBOutlet var arView: ARView!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // 1. Fire off plane detection
        startPlaneDetection()
        
        // 2. 2D Point
        arView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(handleTap(recognizer: ))))
        
        
        // Do any additional setup after loading the view.
    }
    
    @objc func handleTap(recognizer: UITapGestureRecognizer) {
        // Touch location
        let tapLocation = recognizer.location(in: arView)
        
        // Raycast (2D -> 3D)
        let results = arView.raycast(from: tapLocation, allowing: .estimatedPlane, alignment: .horizontal)
        
        if let firstResult = results.first {
            // 3d point (x,y,z)
            let worldPos = simd_make_float3(firstResult.worldTransform.columns.3)
            
            // Create Sphere
            let sphere = createSphere()
            
            // Place the object
            placeObject(object: sphere, at: worldPos)
        }
    }
    
    func placeObject(object: ModelEntity, at location: SIMD3<Float>){
        // 1. Anchor
        let objAnchor = AnchorEntity(world: location)
        
        // 2. Tie model to anchor
        objAnchor.addChild(object)
        
        // 3. Add anchor to scene
        arView.scene.addAnchor(objAnchor)
    }

    func startPlaneDetection() {
        arView!.automaticallyConfigureSession = true
        
        let config = ARWorldTrackingConfiguration()
        config.planeDetection = [.horizontal]
        config.environmentTexturing = .automatic
        
        arView.session.run(config)
    }
    
    func createSphere() -> ModelEntity {
        // Mesh
        let sphere = MeshResource.generateSphere(radius: 0.5)
        
        // Assign material
        let sphereMaterial = SimpleMaterial(color: .blue, roughness: 0, isMetallic: true)
        
        // Model Entity
        let sphereEntity = ModelEntity(mesh: sphere, materials: [sphereMaterial])
        
        return sphereEntity
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
