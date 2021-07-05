import React from "react"
import { Col, OverlayTrigger, Row, Tooltip } from "react-bootstrap"
import ClassificationData from "./../../static/methodClassification.json"

import "./../styles/components/classificationCard.scss"

const ClassificationCard = ({ item }) => (
  <OverlayTrigger
    key={ClassificationData.content[item]["name"]}
    placement="bottom"
    overlay={
      <Tooltip id={`tooltip-${item}`}>
        {ClassificationData.content[item]["description"]}
      </Tooltip>
    }
  >
    <Col>
      <button type="button" className="btn tag">
        {ClassificationData.content[item]["name"]}
      </button>
    </Col>
  </OverlayTrigger>
)

const ClassificationRow = ({ itemList, inline }) => (
  <Row className={"classificationTags" + (inline ? "inline" : "")}>
    {itemList.map(item => (
      <div key={item}>
        <ClassificationCard item={item} />
      </div>
    ))}
  </Row>
)

export { ClassificationCard }
export default ClassificationRow
