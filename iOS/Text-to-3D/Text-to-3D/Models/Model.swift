//
//  Model.swift
//  Text-to-3D
//
//  Created by Aditya Sharma on 5/20/23.
//

import SwiftUI

// Model
struct Model: Identifiable, Hashable {
    var id: String = UUID().uuidString
    var prompt: String
    var url: String
    var toggle: Bool
    var size: Int
}

var sampleData: [Model] = [
    .init(prompt: "a dog", url: "dog.obj", toggle: true, size: 1),
    .init(prompt: "a dog", url: "dog.obj", toggle: false, size: 1),
    .init(prompt: "a dog", url: "dog.obj", toggle: true, size: 1),
    .init(prompt: "a dog", url: "dog.obj", toggle: true, size: 1)
]
