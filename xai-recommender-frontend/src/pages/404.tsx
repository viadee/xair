import React from "react"
import { Container } from "react-bootstrap"

import Layout from "../components/layout"
import PageHeading from "../components/pageHeading"

const NotFoundPage = () => (
  <Layout pageInfo={{ pageName: "404: Not found" }}>
    <PageHeading pageTitle="Not found" />
    <Container className="page full">
      <p>You just hit a route that doesn&#39;t exist... the sadness.</p>
    </Container>
  </Layout>
)

export default NotFoundPage
