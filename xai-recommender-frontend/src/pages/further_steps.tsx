import React from "react"
import { Row, Col, Container } from "react-bootstrap"
import Layout from "../components/layout"
import RecommendationContext from "./../context/recommendationContext"

import PageHeading from "../components/pageHeading"
import BoxReferences from "./../components/boxReferences"
import BoxDetailedMethods from "./../components/boxDetailedMethods"

const FurtherStepsPage = ({ props }) => {
  const references = {
    "1":
      "<a href='https://doi.org/10.5281/zenodo.3240529'>Leslie, David (2019): Understanding artificial intelligence ethics and safety. A guide for the responsible design and implementation of AI systems in the public sector. The Alan Turing Institute.</a>",
    "2":
      "<a href='https://arxiv.org/pdf/1911.02508.pdf'>Dylan Slack; Sophie Hilgard; Emily Jia; Sameer Singh; Himabindu Lakkaraju (2020): Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods.</a>",
    "3":
      "<a href='https://towardsdatascience.com/explainable-ai-in-practice-6d82b77bf1a7'>Kangur, Ayla (2020): Explainable AI in practice. How committing to transparency made us deliver better AI products. In: Towards Data Science, 24.12.2020.</a>",
    "4":
      "<a href='https://christophm.github.io/interpretable-ml-book/'>Molnar, Christoph (2020): Interpretable Machine Learning.",
  }

  return (
    <Layout pageInfo={{ pageName: "Further steps" }}>
      <PageHeading
        pageTitle={`Recommendations for further steps`}
        styleFilled={"gray"}
      />
      <Container fluid className="keyvisual gray">
        <Container className="align-items-center">
          <Row>
            <Col md="12" style={{ marginBottom: "1rem" }}>
              <p>
                Um ein erklärbares, nachvollziehbares und faires Modell zu
                erhalten bzw. zu gewährleisten, empfehlen wir folgende Punkte zu
                beachten:
              </p>
              <ul>
                <li>
                  Es sollte eine Visualisierungsmethode für beliebig viele,
                  jedoch für mindestens die kritischen Features (FOI) verwendet
                  werden, sodass ihre Auswirkungen auf das Ergebnis genauer
                  betrachtet werden können.
                </li>
                <li>
                  Um ein besseres Gesamtbild des Modells und eine vollständigere
                  Erklärung zu erhalten, ist neben der Anwendung der empfohlenen
                  Methode die mindestens einer weiteren XAI Methode ratsam. Eine
                  Kombination von lokalen und globalen Methoden ist
                  empfehlenswert, wobei nach dem Local-first Ansatz gehandelt
                  werden sollte [1]. Das Ausführen mehrerer Methoden ist
                  wichtig, da bestimmte XAI Methoden angegriffen und getäuscht
                  werden können, siehe [2]. Unten ist eine Liste weiterer
                  empfohlener XAI Methoden zu finden.
                </li>
                <li>
                  Lokale Erklärungen sollten dabei sowohl für richtig als auch
                  für falsch vorhergesagte Dateninstanzen erzeugt werden; das
                  gibt Aufschlüsse über eine mögliche Verbesserung des Feature
                  Engineerings. [3]
                </li>
                <li>
                  Es ist wichtig, dass die Modellperformance nur in
                  Kenntnisnahme einer globalen Feature Importance Methode
                  betrachtet wird. [3]
                </li>
                <li>
                  Auch wenn das Modell in Betrieb ist sollten die Eingabedaten
                  kontinuierlich auf Änderungen geprüft und überwacht werden, um
                  neuere Entwicklungen widerzuspiegeln, das Modell zu
                  aktualisieren und somit Vertrauen in die Robustheit des
                  Modells zu gewährleisten. [3]
                </li>
              </ul>
            </Col>
          </Row>
        </Container>
        <div className="success-line" />
      </Container>
      <Container fluid style={{ marginTop: "-2.5rem" }}>
        <PageHeading pageTitle={"Other recommended XAI methods"} />
      </Container>

      <Container className="page">
        <RecommendationContext.Consumer>
          {rec => (
            <div>
              {rec.result == null ||
              rec.result.recommendation.length == 0 ? null : (
                <BoxDetailedMethods
                  small={true}
                  orderedMethods={rec.result.recommendation
                    .slice(1)
                    .map(x => x["name"])}
                />
              )}
            </div>
          )}
        </RecommendationContext.Consumer>
      </Container>
      <BoxReferences references={references} />
    </Layout>
  )
}

export default FurtherStepsPage
