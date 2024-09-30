import SwiftUI
import MarkdownUI

struct RecipeView: View {
    @ObservedObject var recipeVM = RecipeViewModel()
    @State private var showingAlert = false

    var heading: some View {
        HStack {
            Text("Recipe")
                .font(.largeTitle)
                .fontWeight(.bold)
                .foregroundStyle(.green)
                .foregroundColor(Color.primary)
            Spacer()
            Image("recipe")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 50, height: 50)
        }
    }
    
    var showRecipeButton: some View {
        VStack(alignment: .center) {
            Spacer()
            Button(action: {
                showingAlert.toggle()
                recipeVM.getRecipe()
            }) {
                Text("Get Recipe Suggestions")
                    .fontWeight(.semibold)
                    .foregroundColor(.white)
                    .padding()
                    .background(Color.green)
                    .cornerRadius(40)
                    .shadow(radius: 10)
            }
            .alert("Loading Recipe Suggestions Using OpenAI's API", isPresented: $showingAlert) {
                Button("Cool", role: .cancel) { }
            }
        }
    }
    
    var body: some View {
        ScrollView {
            heading
            if recipeVM.recipe != nil {
                Markdown(recipeVM.recipe!)
            } else {

                    showRecipeButton
                    Spacer()
                    
                }
            }
        .padding()
    }
}


#Preview {
    RecipeView()
}
