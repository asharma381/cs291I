//
//  Model.swift
//  ARKitDemo
//
//  Created by Aditya Sharma on 6/2/23.
//

import Foundation
import SwiftUI

// Model Objects
struct Model: Identifiable, Hashable {
    var id: String = UUID().uuidString
    var prompt: String
    var url: URL
}

// Database
var data: [Model] = []

