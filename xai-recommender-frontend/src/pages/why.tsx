import React from "react"
import { Row, Col, Container } from "react-bootstrap"
import Layout from "../components/layout"
import RecommendationContext from "../context/recommendationContext"
import { navigate } from "gatsby"
import PageHeading from "../components/pageHeading"
import BoxMethods from "../components/boxMethods"
import {
  AiOutlineCloseSquare,
  AiOutlineCheckSquare,
  AiOutlineRocket,
  AiOutlineTool,
} from "react-icons/ai"
import { BsExclamationCircle } from "react-icons/bs"
import { CgSmileSad, CgSmile } from "react-icons/cg"
import inputConfig from "./../../static/config/frontend_input_config.json"

import "./../styles/pages/why.scss"

class WhyPage extends React.Component {
  static contextType = RecommendationContext

  componentDidMount() {
    console.log("componentDidMount")
    this.styleTable()
  }

  componentDidUpdate() {
    if (this.context.result == null) {
      navigate("/start")
    }
    console.log("componentDidUpdate")
    this.styleTable()
  }

  htmlDecode = input => {
    var e = document.createElement("div")
    input = input.replace('", "', "")
    e.innerHTML = input
    // handle case of empty input
    return e.childNodes.length === 0 ? "" : e.childNodes[0].nodeValue
  }

  styleTable() {
    // checking table
    // check if available, don't style if already already edited
    var editTable =
      document.getElementsByTagName("table")[0] &&
      document.getElementsByTagName("table")[0].rows[0].cells[0].innerHTML ===
        ""
    if (editTable) {
      var rows = document.getElementsByTagName("table")[0].rows
      //header row
      rows[0].cells[0].innerHTML = "<span class='light'>Because of ...</span>"
      for (var c = 1; c < rows[0].cells.length; c++) {
        if (
          rows[0].cells[c].innerHTML ===
          this.context.result.recommendation[0].label
        ) {
          rows[0].cells[c].innerHTML =
            "<span class='rec'>" +
            rows[0].cells[c].innerHTML +
            "</span><br/><span class='light'>is</span>"
        } else {
          rows[0].cells[c].innerHTML =
            rows[0].cells[c].innerHTML + "<br/><span class='light'>is</span>"
        }
      }
      // table content
      for (var i = 1; i < rows.length; i++) {
        for (var c = 0; c < rows[0].cells.length; c++) {
          rows[i].cells[c].innerHTML = this.htmlDecode(
            rows[i].cells[c].innerHTML
          )
        }
      }
    }
  }

  render() {
    let { result } = this.context
    let activeRules = null

    if (result) {
      activeRules = result.active_rules
    }
    return (
      <Layout pageInfo={{ pageName: "Why?" }}>
        {result == null ? null : (
          <>
            <PageHeading
              // pageTitle={`Why was '${result.recommendation[0].label}' recommended?`}
              pageTitle={`How did the results come?`}
              styleFilled={"gray"}
            />
            <Container fluid className="page" id="why">
              <Container fluid className="keyvisual gray">
                <Container className="align-items-center">
                  <Row>
                    <Col md="12" style={{ marginBottom: "1rem" }}>
                      <a id="inputs" />
                      <h2>
                        What inputs were used to determine the suitability of
                        the XAI methods?
                      </h2>
                    </Col>

                    <Col md="6" sm="12" className="critList">
                      <div>
                        <h3>Boolean criteria</h3>
                        {Object.keys(result.inputs_orig)
                          .filter(
                            (key, idx) =>
                              inputConfig[key] &&
                              typeof result.inputs_orig[key] === "boolean"
                          )
                          .map((key, idx) => {
                            return (
                              <div
                                className="inputBool"
                                key={`inputBool-${idx}`}
                              >
                                {result.inputs_orig[key] ? (
                                  <span className="check">
                                    <AiOutlineCheckSquare />
                                  </span>
                                ) : (
                                  <span className="checkNot">
                                    <AiOutlineCloseSquare />
                                  </span>
                                )}
                                <span className="inputLabel">
                                  {inputConfig[key]["label"]}
                                </span>
                              </div>
                            )
                          })}
                      </div>
                    </Col>
                    <Col md="6" sm="12" className="critList">
                      <div>
                        <h3>Other criteria</h3>
                        {Object.keys(result.inputs_processed.fuzzy)
                          .filter(
                            (key, idx) =>
                              result.inputs_processed.fuzzy[key] !== "True" &&
                              result.inputs_processed.fuzzy[key] !== "False" &&
                              inputConfig[key]
                          )
                          .map((key, idx) => (
                            <div
                              className="inputFuzzy"
                              key={`inputFuzzy-${idx}`}
                            >
                              <div className="inputLabel">
                                {inputConfig[key]["label"]}
                              </div>
                              <div>{result.inputs_processed.fuzzy[key]}</div>
                            </div>
                          ))}
                      </div>
                    </Col>
                  </Row>

                  {result.inputs_processed.fuzzy["corr"] !==
                  ("strong" || "strong/very strong") ? null : (
                    <Row className="inputWarning">
                      <Col md="1" sm="1">
                        <BsExclamationCircle />
                      </Col>
                      <Col md="9" sm="11">
                        Your correlation seems to be{" "}
                        {result.inputs_processed.fuzzy["corr"]} (
                        {result.inputs_orig["corr"]})! <br />
                        Maybe you should look at your dataset and adjust your
                        preprocessing if necessary.
                      </Col>
                    </Row>
                  )}
                  {result.inputs_processed.fuzzy["corr_foi"] !==
                  ("strong" || "strong/very strong") ? null : (
                    <Row className="inputWarning">
                      <Col md="1" sm="1">
                        <BsExclamationCircle />
                      </Col>
                      <Col md="9" sm="11">
                        The correlation of your FOI seems to be{" "}
                        {result.inputs_processed.fuzzy["corr_foi"]} (
                        {result.inputs_orig["corr_foi"]})! <br />
                        Maybe you should look at your dataset and adjust your
                        preprocessing if necessary.
                      </Col>
                    </Row>
                  )}
                </Container>

                <div className="success-line" />
              </Container>
              <Container>
                <Row className="section">
                  {result.excluded_methods &&
                  Object.keys(result.excluded_methods).length !== 0 ? (
                    <>
                      <Col md="1">
                        <span>
                          <CgSmileSad />
                        </span>
                      </Col>
                      <Col md="11" id="excluded">
                        <h2>
                          Which methods can <u>not</u> be used?
                        </h2>
                        <ul>
                          {Object.keys(result.excluded_methods).map(
                            (key, idx) => {
                              return (
                                <li key={`excluded-${idx}`}>
                                  <div>{key}: </div>
                                  <div className="reasonBox">
                                    {result.excluded_methods[key].map(
                                      (element, eidx) => (
                                        <div key={`excluded-${eidx}-reason`}>
                                          <span className="checkNot">
                                            <AiOutlineCloseSquare />
                                          </span>
                                          <span>
                                            {inputConfig[element]["label"]}
                                          </span>
                                        </div>
                                      )
                                    )}
                                  </div>
                                </li>
                              )
                            }
                          )}
                        </ul>
                      </Col>
                    </>
                  ) : (
                    <>
                      <Col md="1">
                        <span>
                          <CgSmile />
                        </span>
                      </Col>
                      <Col md="11" id="excluded">
                        <h4>
                          With the given data all XAI methods can be taken into
                          consideration.
                        </h4>
                      </Col>
                    </>
                  )}
                </Row>
                <Row className="section">
                  <Col md="1">
                    <span>
                      <AiOutlineRocket />
                    </span>
                  </Col>
                  <Col md="11">
                    <h2>
                      How was the suitability of the XAI methods evaluated for '
                      {result.inputs_orig["model_name"]}'?
                    </h2>
                  </Col>
                  <Col md="12">
                    <div
                      id="activeRuleTable"
                      dangerouslySetInnerHTML={{ __html: activeRules }}
                    />
                    <p>
                      Note: Some of the criteria listed here may have different
                      values, for example "medium" and "high". This is because
                      the given input value cannot be completely assigned to any
                      term. The characteristics of the inputs are listed{" "}
                      <a href="#inputs">above</a>.
                    </p>
                  </Col>
                </Row>

                <Row className="section">
                  <Col md="1">
                    <span>
                      <AiOutlineTool />
                    </span>
                  </Col>
                  <Col md="11">
                    <h2>Which XAI Methods were taken into consideration?</h2>
                    <BoxMethods
                      currentMethod={this.context.result.recommendation[0].name}
                    />
                  </Col>
                </Row>
              </Container>
            </Container>
          </>
        )}
      </Layout>
    )
  }
}

export default WhyPage
