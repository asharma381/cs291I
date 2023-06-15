//
//  Home.swift
//  Text-to-3D
//
//  Created by Aditya Sharma on 5/20/23.
//

import SwiftUI

struct Main: View {
    @State var selectedTab = "house"
    var body: some View {
        ZStack(alignment: .bottom, content: {
            Color(.white)
                .ignoresSafeArea()
            
//             Custom Tab Bar
            CustomTabBar(selectedTab: $selectedTab)
            
        })
    }
}

struct Home_Previews: PreviewProvider {
    static var previews: some View {
        Main()
    }
}
