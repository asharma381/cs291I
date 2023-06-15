//
//  CustomTabBar.swift
//  Text-to-3D
//
//  Created by Aditya Sharma on 5/20/23.
//

import SwiftUI

struct CustomTabBar: View {
    @Binding var selectedTab: String
    var body: some View {            TabView(selection: $selectedTab) {
        HomeView()
            .tag("house")
        CameraView()
            .tag("camera")
        Text("tab 3")
            .tag("person")
    }
    .ignoresSafeArea()
    .overlay(
        HStack(spacing: 0){
            // Tab Bar Buttons
            TabBarButton(image: "house", selectedTab: $selectedTab)
            TabBarButton(image: "camera", selectedTab: $selectedTab)
            TabBarButton(image: "person", selectedTab: $selectedTab)
        }
            .padding()
            .background(
                Color(.black)
                    .clipShape(TabCurve())
            )
            .cornerRadius(30)
            .padding(.horizontal),
        alignment: .bottom)
    }
}

struct CustomTabBar_Previews: PreviewProvider {
    static var previews: some View {
        Main()
    }
}

struct TabBarButton: View {
    
    var image: String
    @Binding var selectedTab: String
    
    var body: some View {
        
        // Get midpoint for curve animation
        GeometryReader { reader in
            Button(action: {
                // changing tab
                withAnimation {
                    selectedTab = image
                }
            }, label: {
                // filling color if its selected
                Image(systemName: "\(image)")
                    .font(.system(size: 20, weight: .semibold))
                    .foregroundColor(Color.white)
                // lifing view
                    .offset(y: selectedTab == image ? -5 : 0)
            })
            // Max Frame
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        // max height
        .frame(height: 30)
    }
}
