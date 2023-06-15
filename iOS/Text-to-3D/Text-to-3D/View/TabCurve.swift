//
//  TabCurve.swift
//  Text-to-3D
//
//  Created by Aditya Sharma on 5/20/23.
//

import SwiftUI

struct TabCurve: Shape {
    func path(in rect: CGRect) -> Path {
        return Path {path in
            // Drawing curve path
            path.move(to: CGPoint(x: rect.width, y: rect.height))
            path.addLine(to: CGPoint(x: rect.width, y: 0))
            path.addLine(to: CGPoint(x: 0, y: 0))
            path.addLine(to: CGPoint(x: 0, y: rect.height))
            
            let mid = rect.width / 2
            
            path.move(to: CGPoint(x: mid - 40, y: rect.height))
            
            let to = CGPoint(x: mid, y: rect.height - 20)
        }
    }
}

struct TabCurve_Previews: PreviewProvider {
    static var previews: some View {
        Main()
    }
}
