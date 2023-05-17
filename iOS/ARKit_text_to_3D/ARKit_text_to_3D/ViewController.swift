//
//  ViewController.swift
//  ARKitDemo
//
//  Created by Aditya Sharma on 4/10/23.
//

import UIKit
import ARKit
import Foundation

class ViewController: UIViewController, UITextFieldDelegate {

    var APIUrl = ""

    @IBOutlet weak var textField: UITextField!
    @IBOutlet weak var myButton: UIButton!
    @IBOutlet weak var sceneView: ARSCNView!
    @IBOutlet weak var counterLabel: UILabel!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.textField.delegate = self
        myButton.backgroundColor = .systemRed
        myButton.setTitleColor(.white, for: .normal)
        
        let scene = SCNScene()
        sceneView.scene = scene
        
        let tap = UITapGestureRecognizer(target: self, action: #selector(self.handleTap(_:)))
        sceneView.addGestureRecognizer(tap)

    }
    
    @objc func handleTap(_ sender: UITapGestureRecognizer? = nil){
        print("handle tap")
        
        let touchLocation = sender!.location(in: sceneView)
        guard let query = sceneView.raycastQuery(from: touchLocation, allowing: .existingPlaneInfinite, alignment: .any) else {
            return
        }
        let results = sceneView.session.raycast(query)
        guard results.first != nil else {
            print("no surface found")
            return
        }
        
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
    
    @IBAction func didTapButton(){
        var prompt = textField.text!
        print("PROMPT: " + prompt)
        //        let sessionConfig = URLSessionConfiguration.default
//        sessionConfig.timeoutIntervalForRequest = 200.0
//        sessionConfig.timeoutIntervalForResource = 200.0
//        let session = URLSession(configuration: sessionConfig)
        
        
        guard let url = URL(string: APIUrl) else {
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
                print(type(of: path))
                print(path.absoluteString)
                
                if let meshData = meshstr?.data(using: .utf8) {
                    try? meshData.write(to: path)
                }
//                let response = try JSONSerialization.jsonObject(with: data, options: .fragmentsAllowed)
                
                let notebook = Notebook()
                notebook.loadModel(path: path)
                let xPos = self.randomPosition(lowerBound: -1.5, upperBound: 1.5)
                let yPos = self.randomPosition(lowerBound: -1.5, upperBound: 1.5)
                notebook.position = SCNVector3(x: xPos, y: yPos, z: -1)
                self.sceneView.scene.rootNode.addChildNode(notebook)
                
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
        
        sceneView.session.run(config)
        addObject()
    }
    
    func addObject() {
        print("Hello World!")
        let csilURL = "http://128.111.30.211:6969/url"
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
            self.APIUrl = str! + "/text_to_3d"
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
    }
}

