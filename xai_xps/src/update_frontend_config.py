from XAIRecommender import XAIRecommender

if __name__ == '__main__':

    xair = XAIRecommender(verbose=True, reload=True)
    # update current rules text file
    xair.print_rules()