import React from "react"
/*
{
        "recommendation": [],
        "active_rules": [],
        "excluded_methods": [],
    }
    */

var defaultContext = {
  result: null,
  changeResult: res => {},
}

const RecommendationContext = React.createContext(defaultContext)

class RecommendationProvider extends React.Component {
  state = {
    result: null,
  }

  componentDidMount() {
    // Getting value from sessionStorage!
    console.log("Getting recommendation value from sessionStorage!")
    const recRes = JSON.parse(sessionStorage.getItem("recommendationResult"))
    console.log(recRes)
    this.setState({ result: recRes }, () => console.log(this.state))
  }

  changeResult = result => {
    sessionStorage.setItem("recommendationResult", JSON.stringify(result))
    this.setState({ result }, () => console.log(this.state))
  }

  render() {
    const { result } = this.state
    return (
      <RecommendationContext.Provider
        value={{
          result,
          changeResult: res => this.changeResult(res),
        }}
      >
        {this.props.children}
      </RecommendationContext.Provider>
    )
  }
}

// export const RecommendationConsumer = RecommendationContext.Consumer

export default RecommendationContext
export { RecommendationProvider }
