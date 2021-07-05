import React, { useEffect } from "react"
import Layout from "../components/layout"
import PageHeading from "../components/pageHeading"
import { Container, Row, Col } from "react-bootstrap"

const Feedback = () => {
  useEffect(() => {
    const script = document.createElement("script")
    // if IE6-11
    if (/*@cc_on!@*/ false || !!document.documentMode) {
      script.src = "https://js.hsforms.net/forms/v2-legacy.js"
    } else {
      script.src = "https://js.hsforms.net/forms/v2.js"
    }

    document.body.appendChild(script)

    script.addEventListener("load", () => {
      if (window.hbspt) {
        window.hbspt.forms.create({
          region: "na1",
          portalId: "3993578",
          formId: "ab989771-26de-480c-92ff-0cc7f6cc205e",
          target: "#hubspotForm",
        })
      }
    })
  })

  return (
    <Layout pageInfo={{ pageName: "Start" }}>
      <PageHeading pageTitle="Feedback for XAI Recommender" />
      <Container>
        <Row style={{ marginBottom: "2rem", marginTop: "2rem" }}>
          <Col md="12">
            <h1>Thank you for your feedback. We appreciate your help!</h1>
          </Col>

          <Col md="12">
            <div id="hubspotForm"></div>
          </Col>
        </Row>
      </Container>
    </Layout>
  )
}

export default Feedback
