import React from "react"
import Layout from "./../components/layout"
import { Row, Col, Container } from "react-bootstrap"
import PageHeading from "./../components/pageHeading"
import {
  AiOutlineTags,
  AiOutlineQuestionCircle,
  AiOutlineCheckCircle,
  AiOutlineInfoCircle,
} from "react-icons/ai"
import { BiRightArrow } from "react-icons/bi"
import ClassificationRow from "./../components/classificationCard"
import { VscSettingsGear } from "react-icons/vsc"
import { BsExclamationCircle } from "react-icons/bs"
import BoxReferences from "./../components/boxReferences"
import BoxMethods from "../components/boxMethods"
import { Link } from "gatsby"

const Method = ({ pageContext }) => {
  const { method } = pageContext

  return (
    <Layout pageInfo={{ pageName: `Method ${method.abbr}` }}>
      <PageHeading
        pageTitle={
          method.abbr.toLowerCase() !== method.name.toLowerCase()
            ? `${method.abbr} (${method.name})`
            : `${method.name}`
        }
      />
      <Container id="method">
        <Row className="section">
          <Col md="1">
            <span>
              <AiOutlineTags />
            </span>
          </Col>
          <Col md="11">
            <h2>Taxonomische Einordnung</h2>
            <div className="classification">
              <ClassificationRow itemList={method.classification} />
            </div>
            <Col className="linkBox">
              <div>
                <BiRightArrow />
                <Link to={`/implementation/${method.id}`}>
                  Welche Implementierung wird empfohlen?
                </Link>
              </div>
            </Col>
          </Col>
        </Row>
        <Row className="section">
          <Col md="1">
            <span>
              <AiOutlineQuestionCircle />
            </span>
          </Col>
          <Col md="11">
            <h2>Welche Frage beantwortet {method.abbr}?</h2>
            <div
              className="text"
              dangerouslySetInnerHTML={{ __html: method.question }}
            />
            <div
              className="question-example"
              dangerouslySetInnerHTML={{ __html: method.questionExample }}
            />
          </Col>
        </Row>
        <Row className="section">
          <Col md="1">
            <span>
              <VscSettingsGear />
            </span>
          </Col>
          <Col md="11">
            <h2>Wie funktioniert {method.abbr}?</h2>
            <div
              className="text"
              dangerouslySetInnerHTML={{ __html: method.function }}
            />
          </Col>
        </Row>
        <Row className="section border">
          <Col md="1">
            <span>
              <AiOutlineCheckCircle />
            </span>
          </Col>
          <Col md="11">
            <h2>Was ist das Ergebnis von {method.abbr}?</h2>
            <div
              className="text"
              dangerouslySetInnerHTML={{ __html: method.result }}
            />
          </Col>
          <Col md="12" className="images">
            <img
              src={method.resultImg}
              alt={"Ergebnisdarstellung " + method.abbr}
            />
            <p className="subtitle">Ergebnisdarstellung {method.abbr}</p>
          </Col>
        </Row>
        {method.noQuestion && method.noQuestion !== "" ? (
          <Row className="section">
            <Col md="1">
              <span>
                <BsExclamationCircle />
              </span>
            </Col>
            <Col md="11">
              <h2>
                Welche Frage beantwortet {method.abbr} <u>nicht</u>?
              </h2>
              <div
                className="text"
                dangerouslySetInnerHTML={{ __html: method.noQuestion }}
              />
            </Col>
          </Row>
        ) : null}

        <Row className="section">
          <Col md="1">
            <span>
              <BiRightArrow />
            </span>
          </Col>
          <Col md="11">
            <Link to={`/implementation/${method.id}`}>
              <h2>Welche Implementierung wird empfohlen?</h2>
            </Link>
          </Col>
        </Row>

        <Row className="section">
          <Col md="1">
            <span>
              <AiOutlineInfoCircle />
            </span>
          </Col>
          <Col md="11">
            <h2>Weitere Methoden</h2>
            <BoxMethods excludeMethods={[method.id]} />
          </Col>
        </Row>
      </Container>
      <BoxReferences references={method.references} />
    </Layout>
  )
}

export default Method
