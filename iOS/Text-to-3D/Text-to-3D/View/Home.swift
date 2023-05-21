//
//  Home.swift
//  Text-to-3D
//
//  Created by Aditya Sharma on 5/20/23.
//

import SwiftUI

struct Home: View {
    @State var selectedTab = "house"
    var body: some View {
        ZStack(alignment: .bottom, content: {
            Color(.white)
                .ignoresSafeArea()
            
//             Custom Tab Bar
            CustomTabBar(selectedTab: $selectedTab)
            
        })
        
        
//        TabView {
//            Text("item1")
//                .tabItem {
//                    Label("One", systemImage: "star")
//                }
//            Text("item2")
//                .tabItem{
//                    Label("Two", systemImage: "circle")
//                }
//        }
    }
}

struct Home_Previews: PreviewProvider {
    static var previews: some View {
        Home()
    }
}
