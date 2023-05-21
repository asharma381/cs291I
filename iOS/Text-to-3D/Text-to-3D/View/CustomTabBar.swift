//
//  CustomTabBar.swift
//  Text-to-3D
//
//  Created by Aditya Sharma on 5/20/23.
//

import SwiftUI

struct CustomTabBar: View {
    @Binding var selectedTab: String
    var body: some View {
        VStack {
            TabView(selection: $selectedTab) {
                Text("tab 1")
                    .tag("house")
                Text("tab 2")
                    .tag("camera")
                Text("tab 3")
                    .tag("person")
            }
            
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
            .padding(.horizontal)
                
        }
    }
}

struct CustomTabBar_Previews: PreviewProvider {
    static var previews: some View {
        Home()
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
                Image(systemName: "\(image)\(selectedTab == image ? ".fill" : "")")
                    .font(.system(size: 25, weight: .semibold))
                    .foregroundColor(Color.white)
                // lifing view
                    .offset(y: selectedTab == image ? -10 : 0)
            })
            // Max Frame
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        // max height
        .frame(height: 50)
    }
}
