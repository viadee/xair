import React from "react"
import { Container } from "react-bootstrap"

import Layout from "../components/layout"
import PageHeading from "../components/pageHeading"

const NotFoundPage = () => (
  <Layout pageInfo={{ pageName: "Oops" }}>
    <PageHeading pageTitle="An error occurred... " />
    <Container className="page full">
      <h2>
        Sometimes even systems without AI inexplicably don't work as they should
        ...
      </h2>
      <p>Please refresh the side and try again..</p>
      <p>
        If the problems remain, please{" "}
        <a href="mailto:verena.barth@viadee.de">contact me</a>{" "}
      </p>
    </Container>
  </Layout>
)

export default NotFoundPage
