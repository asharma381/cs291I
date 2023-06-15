//
//  ViewController.swift
//  ARKitDemo
//
//  Created by Aditya Sharma on 4/10/23.
//

import UIKit
import SwiftUI
import ARKit
import Foundation
import InstantSearchVoiceOverlay

class ViewController: UIViewController, UITextFieldDelegate {

    let voiceOverlay = VoiceOverlayController()
    var dot = UIView(frame: CGRect(x: -100, y: -100, width: 20, height: 20))
    var APIUrl = ""
    var path: URL!
    var modelPrompt: String!
    var notebook = Notebook()
    let sUIVC = SwiftUIViewController()
    
    var xPos: Float = 0.0
    var yPos: Float = 0.0
    var zPos: Float = 0.0
    
    var display: Bool!

    @IBOutlet weak var textField: UITextField!
    @IBOutlet weak var myButton: UIButton!
    @IBOutlet weak var uiButton: UIButton!
    @IBOutlet weak var sceneView: ARSCNView!
    @IBOutlet weak var counterLabel: UILabel!
    @IBOutlet weak var mySwitch: UISwitch!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.textField.delegate = self
        
        display = false
        
        let scene = SCNScene()
        sceneView.scene = scene
        
        let tap = UITapGestureRecognizer(target: self, action: #selector(self.handleTap(_:)))
        sceneView.addGestureRecognizer(tap)
        
        dot.backgroundColor = .cyan
        dot.layer.cornerRadius = 10
        
        // customize textField
        textField.placeholder = "Enter Prompt (e.g. cake)"
        textField.frame = CGRectMake(UIScreen.main.bounds.width * 0.075, UIScreen.main.bounds.height * 0.075, 200, 35)
        
        // customize button
        myButton.setTitle("Submit", for: .normal)
        myButton.setTitleColor(.white, for: .normal)
        let bWidth = CGFloat(100), bHeight = CGFloat(35)
        myButton.frame = CGRectMake(UIScreen.main.bounds.width * 0.8 - bWidth/2, UIScreen.main.bounds.height * 0.075, bWidth, bHeight)
        myButton.backgroundColor = .blue
        myButton.layer.cornerRadius = 5
        
        // customize switch
        mySwitch.frame = CGRectMake(UIScreen.main.bounds.width * 0.8, UIScreen.main.bounds.height * 0.85, 49, 31)
        mySwitch.addTarget(self, action: #selector(self.switchStateDidChange(_:)), for: .valueChanged)
        mySwitch.setOn(true, animated: false)
        
        // customize ui button
        uiButton.frame = CGRectMake(UIScreen.main.bounds.width * 0.075, UIScreen.main.bounds.height * 0.85, bWidth, bHeight)
        uiButton.layer.cornerRadius = 5
        uiButton.isHidden = true
        
        // experimental .mtl files and .obj
//        let pot = SCNScene(named: "pot.obj")
//        let material = SCNMaterial()
//        material.diffuse.contents = "pot.jpg"
//
//        let potNode = SCNNode()
//        potNode.geometry?.materials = [material]
//
//        for child in pot!.rootNode.childNodes {
//            potNode.addChildNode(child)
//        }
//        sceneView.scene.rootNode.addChildNode(potNode)
        
    }
    
    @objc func switchStateDidChange(_ sender: UISwitch!) {
        if sender.isOn == true {
            self.textField.isHidden = false
            self.myButton.isHidden = false
            self.dot.isHidden = false
            self.uiButton.isHidden = false
        } else {
            self.textField.isHidden = true
            self.myButton.isHidden = true
            self.dot.isHidden = true
            self.uiButton.isHidden = true
        }
    }
    
    @objc func handleTap(_ sender: UITapGestureRecognizer? = nil){
//        print("handle tap")
//
//        let touchLocation = sender!.location(in: sceneView)
//        guard let query = sceneView.raycastQuery(from: touchLocation, allowing: .existingPlaneInfinite, alignment: .any) else {
//            return
//        }
//        let results = sceneView.session.raycast(query)
//        guard results.first != nil else {
//            print("no surface found")
//            return
//        }
//
//        let cube = createCubeNode()
//        cube.transform = SCNMatrix4(results.first!.worldTransform)
//        sceneView.scene.rootNode.addChildNode(cube)
        
//        if let node = results.first?.node as SCNNode? {
//            node.removeFromParentNode()
//        }
        
//        let hitResults = sceneView.hitTest(touchLocation, types: [.featurePoint])
//        sceneView.session.raycast(<#T##query: ARRaycastQuery##ARRaycastQuery#>)
//        if hitResults.count > 0 {
//            if let node = hitResults.first?.node as SCNNode? {
//                node.removeFromParentNode()
//            }
//        }
        
        //        let touchLocation = UITapGestureRecognizer.location(in: sceneView)
        //        sceneView.scene.rootNode.enumerateChildNodes { (node, _) in
        //            node.removeFromParentNode()
        //        }
    }
    
    private func createCubeNode() -> SCNNode {
        // create the basic geometry of the box (sizes are in meters)
        let boxGeometry = SCNBox(width: 0.1, height: 0.1, length: 0.1, chamferRadius: 0)

        // give the box a material to make a little more realistic
        let material = SCNMaterial()
        material.diffuse.contents = UIColor.blue
        material.specular.contents = UIColor(white: 0.6, alpha: 1.0)

        // create the node and give it the materials
        let boxNode = SCNNode(geometry: boxGeometry)
        boxNode.geometry?.materials = [material]

        return boxNode
    }
    
    @IBAction func didTapButton(){
        print("NGROK URL: \(APIUrl)")
        let prompt = textField.text!
        modelPrompt = prompt
        print("PROMPT: " + prompt)

        // convert image from ARSCNView to UIImage
        let convertedImage = imageFrom(scene: sceneView)
        guard let imageData = convertedImage.jpegData(compressionQuality: 0.1) else {
            return
        }
        
        let base64Encoded = imageData.base64EncodedString()
        print(base64Encoded)

        guard let imgUrl = URL(string: APIUrl + "/get_placement") else {return}
        print("IMAGE URL: \(imgUrl)")
        print("SENDING REQUEST")
        
        var imgRequest = URLRequest(url: imgUrl, timeoutInterval: 200.0)
        imgRequest.httpMethod = "POST"
        
        let uuid = UUID().uuidString
        let CRLF = "\r\n"
        let fileName = uuid + ".jpg"
//        let formName = "file"
//        let type = "image/jpeg"
        var imgBody = Data()
        
        imgRequest.setValue("multipart/form-data; boundary=\(uuid)", forHTTPHeaderField: "Content-Type")
        imgBody.append("\r\n--\(uuid)\r\n".data(using: .utf8)!)
        imgBody.append("Content-Disposition: form-data; name=\"file\"; filename=\"recieved\(fileName)\"\r\n".data(using: .utf8)!)
        imgBody.append(("Content-Type: \" content-type header" + CRLF + CRLF).data(using: .utf8)!)
        imgBody.append("<ENCODING>".data(using: .utf8)!)
        imgBody.append((base64Encoded).data(using: .utf8)!)
        imgBody.append("</ENCODING>".data(using: .utf8)!)
        imgBody.append("<PROMPT>".data(using: .utf8)!)
        imgBody.append((prompt).data(using: .utf8)!)
        imgBody.append("</PROMPT>".data(using: .utf8)!)
        imgBody.append("\r\n--\(uuid)\r\n".data(using: .utf8)!)
        
//        imgBody.append((CRLF).data(using: .utf8)!)
//        imgBody.append("Content-Disposition: form-data; name=\"formName\"; filename=\"\(fileName)\"\r\n".data(using: .utf8)!)
//        imgBody.append(("Content-Type: \(type)" + CRLF + CRLF).data(using: .utf8)!)
//        imgBody.append(imageData as Data)
//        imgBody.append(["image": base64Encoxded])
        imgRequest.httpBody = imgBody
        
//        imgRequest.setValue("application.json", forHTTPHeaderField: "Content-Type")
//        let imgBody: [String: (CGFloat) -> Data?] = [
//            "upload_file" : imageRep,
//        ]
//        imgRequest.httpBody = try? JSONSerialization.data(withJSONObject: imgBody, options: .fragmentsAllowed)
        
        // UPLOAD TASK
//        URLSession.shared.uploadTask(with: imgRequest, from: imgBody, completionHandler: {responseData, response, error in
//            if error == nil {
//                print("OBJ")
//                let jsonData = try? JSONSerialization.jsonObject(with: responseData!, options: .allowFragments)
//                if let json = jsonData as? [String: Any] {
//                    Swift.print(json)
//                }
//            }
//        }).resume()
                                
    
        let imgTask = URLSession.shared.dataTask(with: imgRequest) {data,_,error in
            guard let data = data, error == nil else {
                return
            }
            print("SENT IMAGE...")
            
            do {
                // parse response
                let json = try JSONSerialization.jsonObject(with: data, options: .allowFragments) as! [String: Any]
                // var response = String(data: data, encoding: .utf8)
                // print(response!)
//                let x = (json["x"] as! NSString).doubleValue
//                let y = (json["y"] as! NSString).doubleValue
                let x = json["x"] as! Double
                let y = json["y"] as! Double
                
                print(x)
                print(y)

//                guard let query = self.sceneView.raycastQuery(from: CGPoint(x: x, y: y), allowing: .estimatedPlane, alignment: .horizontal) else{
//                    print("Couldn't create a query!")
//                    return
//                }
                guard let raycastQuery = self.sceneView.raycastQuery(
                    from: CGPoint(x: x/3, y: y/3),
                    allowing: .existingPlaneInfinite,
                    alignment: .any) else {return}
                print("Q: ", raycastQuery)
                print("(x,y,z)", raycastQuery.origin)

                guard let raycastResult = self.sceneView.session.raycast(
                    raycastQuery).first else { print("res returning"); return }

                
                print("res: ", raycastResult)
//                print("transform: ", raycastResult.worldTransform)
                self.xPos = raycastResult.worldTransform.columns.3.x
                self.yPos = raycastResult.worldTransform.columns.3.y
                self.zPos = raycastResult.worldTransform.columns.3.z
                print("x: ", self.xPos)
                print("y: ", self.yPos)
                print("z: ", self.zPos)
                
                
//                let sphere = SCNSphere(radius: 0.1)
//                let sphereNode = SCNNode()
//                sphereNode.geometry = sphere
//                sphereNode.position = SCNVector3(x: self.xPos, y: self.yPos, z: raycastResult.worldTransform.columns.3.z)
//                sphereNode.transform = SCNMatrix4(raycastResult.worldTransform)
                
//                self.sceneView.scene.rootNode.addChildNode(sphereNode)
                
//                let notebook = Notebook()
//                notebook.loadModel()
//                notebook.transform = SCNMatrix4(result.worldTransform)
//                self.sceneView.scene.rootNode.addChildNode(notebook)
                
                // 1 point = 4 pixels (div by 2)
                DispatchQueue.main.async {
                    print("moving to (x:", x/3, " y:", y/3, ")")
                    self.dot.frame = CGRect(x: x/3, y: y/3, width: self.dot.frame.width, height: self.dot.frame.height)
//                    self.myButton.frame = CGRectMake(x/3, y/3, self.myButton.frame.width, self.myButton.frame.height)
                    
                    print("WIDTH: ", UIScreen.main.bounds.width)
                    print("HEIGHT: ", UIScreen.main.bounds.height)

//                    var dot = UIView(frame: CGRect(x: x/3, y: y/3, width: 20, height: 20))
                    self.dot.backgroundColor = .cyan
                    self.dot.layer.cornerRadius = 10
                    self.sceneView.addSubview(self.dot)
                    self.modelPrompt = prompt
                    
//                    guard let currentFrame = self.sceneView.session.currentFrame,
//                          let hitTest = currentFrame.hitTest(CGPoint(x: x/3, y: y/3), types: .featurePoint).last else {
//                        return
//                    }
//                    let anchor = ARAnchor(transform: hitTest.worldTransform)
//                    self.sceneView.session.add(anchor: anchor)
                    
                    self.notebook.position = SCNVector3(x: self.xPos, y: self.yPos, z: self.zPos)
                    self.notebook.scale = SCNVector3(x: 0.1, y: 0.1, z: 0.1)
                    
                    let orientation = self.notebook.orientation
                    var glQuat = GLKQuaternionMake(orientation.x, orientation.y, orientation.z, orientation.w)
                    // rotate about z
                    let multi = GLKQuaternionMakeWithAngleAndAxis(-.pi/2, 1, 0, 0)
                    glQuat = GLKQuaternionMultiply(glQuat, multi)
                    self.notebook.orientation = SCNQuaternion(x: glQuat.x, y: glQuat.y, z: glQuat.z, w: glQuat.w)

                    self.sceneView.scene.rootNode.addChildNode(self.notebook)
                }
            
                
                
            } catch let error as NSError {
                print(error)
            }
            
        }
        imgTask.resume()
        // Computer Vision -- 2D image to understand the 3D real world
        // Visual Coherence --
        // Visualization -- Graphics
        
        //        let sessionConfig = URLSessionConfiguration.default
//        sessionConfig.timeoutIntervalForRequest = 200.0
//        sessionConfig.timeoutIntervalForResource = 200.0
//        let session = URLSession(configuration: sessionConfig)
        
        
        guard let url = URL(string: APIUrl + "/text_to_3d") else {
            return
        }
        print("----------------------------")
        print("MAKING API for text-to-3d...")
        print("----------------------------")
        print("NGROK URL: \(APIUrl)")
        var request = URLRequest(url: url, timeoutInterval: 200.0)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        let body: [String: AnyHashable] = [
            "prompt" : prompt,
        ]
        print("prompt = \(prompt)")
        request.httpBody = try? JSONSerialization.data(withJSONObject: body, options: .fragmentsAllowed)
        
        let task = URLSession.shared.dataTask(with: request) { data, _, error in
            guard let data = data, error == nil else {
                return
            }
            
            do {
                print("BEFORE RESPONSE...")
                var meshstr = String(data: data, encoding: .utf8)
//                print(meshstr!)
                
                let path = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0].appendingPathComponent("\(prompt).obj")
                
                print("PATH:")
                print(path)
//                print(type(of: path))
                print(path.absoluteString)
                
                if let meshData = meshstr?.data(using: .utf8) {
                    try? meshData.write(to: path)
                }
//                let response = try JSONSerialization.jsonObject(with: data, options: .fragmentsAllowed)
                
                // COMMENTING THIS OUT FOR NOW
                self.notebook = Notebook()
                self.notebook.loadModel(path: path)
                self.sUIVC.path = path
                self.sUIVC.display = true
                self.display = true
                self.path = path
                self.uiButton.isHidden = false
//                let xPos = self.randomPosition(lowerBound: -1.5, upperBound: 1.5)
//                let yPos = self.randomPosition(lowerBound: -1.5, upperBound: 1.5)
                
                print("SUCCESS")
            }
            catch {
                print(error)
            }
        }
        task.resume()
        
//        voiceOverlay.start(on: self, textHandler: { text, final, _ in
//            if final {
//                print("Final text: \(text)")
//            }else{
//                print("In progress: \(text)")
//            }
//        }, errorHandler: {error in
//
//        })
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        let config = ARWorldTrackingConfiguration()
        config.planeDetection = .horizontal
        
        sceneView.delegate = self
        sceneView.session.delegate = self
//        sceneView.debugOptions = [ARSCNDebugOptions.showFeaturePoints, ARSCNDebugOptions.showWorldOrigin]
        sceneView.debugOptions = [ARSCNDebugOptions.showFeaturePoints]
        sceneView.session.run(config)
        addObject()
    }
    
    func imageFrom(scene: ARSCNView) -> UIImage {
        print("convert ARSCNView to UIImage...")
        UIGraphicsBeginImageContextWithOptions(scene.bounds.size, scene.isOpaque, 0.0)
        scene.drawHierarchy(in: scene.bounds, afterScreenUpdates: false)
        let image = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()
        let uiImage = UIImage(cgImage: (image?.cgImage)!)
        print("Converted to UIImage")
        return uiImage
    }
    
    func addObject() {
        print("Hello World!")
        let csilURL = "http://128.111.30.213:6969/url"
        let request = NSMutableURLRequest(url: NSURL(string: csilURL)! as URL,
                                                cachePolicy: .useProtocolCachePolicy,
                                            timeoutInterval: 10.0)
        request.httpMethod = "GET"

        let session = URLSession.shared
        let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
          if (error != nil) {
            print(error)
          } else {
            let httpResponse = response as? HTTPURLResponse
            print(httpResponse)
            let data = data
            let str = String(data: data!, encoding: .utf8)
            print(str)
            self.APIUrl = str!

              //            self.APIUrl = str! + "/text_to_3d"
            self.counterLabel.text = str
          }
        })

        dataTask.resume()
    }
    
    func randomPosition(lowerBound lower:Float, upperBound upper:Float) -> Float {
        return Float(arc4random()) / Float(UInt32.max) * (lower - upper) + upper
    }

    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        return textField.resignFirstResponder()
    }
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        self.view.endEditing(true)
        
        
        guard let location = touches.first?.location(in: sceneView) else {
              print("Couldn't find location!")
              return
        }
        
        print("Tapped Location: ", location.x, ",", location.y)

        guard let query = sceneView.raycastQuery(from: location, allowing: .estimatedPlane, alignment: .horizontal) else {
              print("Couldn't create a query!")
              return
        }
        
        print("Q: ", query)
        print("(x,y,z)", query.origin)
        print(sceneView.session.raycast(query))

        guard let result = sceneView.session.raycast(query).first else {
              print("Couldn't match the raycast with a plane.")
              return
        }
        
//        let cube = createCubeNode()
//        cube.transform = SCNMatrix4(result.worldTransform)
//        sceneView.scene.rootNode.addChildNode(cube)
        
//        print(result.world)
//        let notebook = Notebook()
//        query.
//        notebook.loadModel()
//        let xPos = self.randomPosition(lowerBound: -1.5, upperBound: 1.5)
//        let yPos = self.randomPosition(lowerBound: -1.5, upperBound: 1.5)
//        notebook.transform = SCNMatrix4(result.worldTransform)
//        notebook.position = SCNVector3(x: query.origin.x, y: query.origin.y, z: query.origin.z)
//        self.sceneView.scene.rootNode.addChildNode(notebook)
        
    }
    
    @IBAction func tapUIButton(){
        // swiftUI interop
        if(sUIVC.display && display){
            let vc = UIHostingController(rootView: SwiftUIView(path: self.path, prompt: self.modelPrompt))
            present(vc, animated: true)
        }else{
            print("must wait, cannot display yet :)")
        }
    }

}


extension ViewController: ARSCNViewDelegate, ARSessionDelegate {
    func renderer(_ renderer: SCNSceneRenderer, didAdd node: SCNNode, for anchor: ARAnchor) {
        // TODO: Add code
//        guard let planeAnchor = anchor as? ARPlaneAnchor else { return }
//
//        // Create a custom object to visualize the plane geometry and extent.
//        let plane = Plane(anchor: planeAnchor, in: sceneView)
//
//        // Add the visualization to the ARKit-managed node so that it tracks
//        // changes in the plane anchor as plane estimation continues.
//        node.addChildNode(plane)
    }
    
    func renderer(_ renderer: SCNSceneRenderer, didUpdate node: SCNNode, for anchor: ARAnchor) {
//        print(node)
//        guard let planeAnchor = anchor as? ARPlaneAnchor,
//              let planeNode = node.childNodes.first
//              let plane = planeNode.geometry as? SCNPlane
//        else { print("returning"); return }
        
//        print(planeAnchor)
//        print(planeNode)
//        let width = CGFloat(planeAnchor.extent.x)
//        let height = CGFloat(planeAnchor.extent.z)
//        plane.width = width
//        plane.height = height
        
//        let x = CGFloat(planeAnchor.center.x)
//        let y = CGFloat(planeAnchor.center.y)
//        let z = CGFloat(planeAnchor.center.z)
//        planeNode.position = SCNVector3(x, y, z)
//        print("Position: ", x, y, z)
    }
}
