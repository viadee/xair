import React from "react"
import { Row, Col, Container, OverlayTrigger, Tooltip } from "react-bootstrap"
import Layout from "../components/layout"
import RecommendationContext from "../context/recommendationContext"
import { Link, navigate, StaticQuery } from "gatsby"
import PageHeading from "../components/pageHeading"
import { BiRightArrow } from "react-icons/bi"
import { useStaticQuery, graphql } from "gatsby"

import "./../styles/pages/result.scss"

type ResultPageProps = {
  bla: string
}

class ResultPage extends React.Component<ResultPageProps> {
  static contextType = RecommendationContext

  constructor(props) {
    super(props)
    this.barChart = this.barChart.bind(this)
  }

  componentDidMount() {
    if (this.context.result == null) {
      navigate("/start")
    }
  }

  componentDidUpdate() {
    console.log(this.context)
    if (this.context.result == null) {
      navigate("/start")
    }
  }

  barChart() {
    const rec = this.context.result.recommendation

    if (rec.length == 1) {
      return (
        <div className="methodContainer">
          <h1>{rec[0]["label"]}</h1>
        </div>
      )
    } else {
      // get unique rating values
      // if there's only one rating: all same height (50%)
      // if there are two ratings: don't make height difference too high
      let uniqueRatings = new Set()
      rec.forEach(r => uniqueRatings.add(r["rating"]))

      // get lowest, take as 0
      var lowest = rec[rec.length - 1]["rating"]
      // get highest, take as 100
      var highest = rec[0]["rating"]

      return (
        <div className="methodBarContainer">
          {rec.map((method, index) => {
            if (uniqueRatings.size == 1) {
              // if all equal, put all to 50%
              var height = "50"
            } else {
              // get scaled percentage for height of bar
              height = Number(
                ((method["rating"] - lowest) / (highest - lowest)) * 100
              ).toFixed(0)
              if (uniqueRatings.size == 2) {
                height = height === "0" ? "40" : height
              } else {
                height = height === "0" ? "1" : height
              }
            }

            var prop = this.props.methods.find(
              x =>
                x.context.method.abbr.toLowerCase() ===
                method.label.toLowerCase()
            )
            return (
              <OverlayTrigger
                trigger={["hover", "focus"]}
                key={index}
                placement="bottom"
                overlay={
                  <Tooltip id={`tooltip-${index}`}>
                    <b>{prop.context.method.name}</b>
                    <br />
                    beantwortet die Frage:
                    <div
                      className="tooltipText italic"
                      dangerouslySetInnerHTML={{
                        __html: prop.context.method.question,
                      }}
                    />
                  </Tooltip>
                }
              >
                <a href={prop.path}>
                  <div className="methodBar" key={index}>
                    <div className="name">{method.label}</div>
                    <div className="rating" style={{ height: `${height}%` }} />
                  </div>
                </a>
              </OverlayTrigger>
            )
          })}
          {/*<div className="line5" style={{bottom: `${line}%`}} />*/}
        </div>
      )
    }
  }

  render() {
    let { result } = this.context
    console.log(this.props)

    return (
      <Layout pageInfo={{ pageName: "Recommendation result" }}>
        <PageHeading
          pageTitle="Recommendation result"
          styleFilled={"colored"}
        />
        <Container fluid className="page" id="result">
          {result == null || result.recommendation.length == 0 ? null : (
            /*(
                <div className="noResult">
                <h1>
                  No result yet. Please insert parameters or request existing recommendation via URL
                </h1>
                <p>
                <Link to="/start">Insert parameters</Link>
                </p>
                </div>

              ) */
            <>
              <Container fluid className="keyvisual gradient-background">
                <Row className="align-items-center">
                  <Col>{this.barChart()}</Col>
                </Row>
                <div className="success-line" />
              </Container>
              <Container>
                <Row>
                  <Col md="12">
                    <h1>How to continue now?</h1>
                    <p>
                      Please take a look at the suggested steps in the
                      navigation bar above.
                      <br />
                      The answers to some questions you may have can be found
                      here:{" "}
                    </p>
                  </Col>
                  <Col className="linkBox">
                    <div>
                      <BiRightArrow />
                      <Link to="/why">How was the result determined?</Link>
                    </div>
                    <div>
                      <BiRightArrow />
                      <Link to="/faq#howdoesitwork">
                        How does the recommender work?
                      </Link>
                    </div>
                  </Col>
                </Row>
              </Container>
            </>
          )}
        </Container>
      </Layout>
    )
  }
}

//export default ResultPage

export default props => (
  <StaticQuery
    query={graphql`
      query ResultMethodQuery {
        allSitePage(filter: {context: {method: {id: {regex: "/.*\\S.*/"}}}}) {
          nodes {
              context {
              method {
                  abbr
                  name
                  question
              }
              }
              path
          }
        }
    }
    `}
    render={data => <ResultPage methods={data.allSitePage.nodes} {...props} />}
  />
)
