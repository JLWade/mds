import React from "react";
import PropTypes from "prop-types";
import { TENURE, NO_MINE, MINER_TWO, PERMIT, GROUP_MINERS } from "@/constants/assets";
import * as String from "@/constants/strings";

/**
 * @constant NullScreen is a reusable view for when there is no data to display, add more views when required.
 */

const propTypes = {
  type: PropTypes.oneOf([
    "dashboard",
    "generic",
    "manager",
    "manager-small",
    "tenure",
    "permit",
    "no-results",
    "unauthorized",
    "view-mine-manager",
    "contacts",
  ]),
};

const NullScreen = (props) => (
  <div className="null-screen">
    {props.type === "dashboard" && (
      <div>
        <img src={NO_MINE} />
        <h3>{String.NO_DATA}</h3>
        <p>{String.TRY_AGAIN}</p>
      </div>
    )}
    {props.type === "generic" && (
      <div>
        <img src={NO_MINE} />
        <h3>{String.NO_DATA}</h3>
      </div>
    )}
    {props.type === "manager" && (
      <div className="null-screen--inline">
        <img src={MINER_TWO} />
        <h3>{String.NO_MINE_MANAGER}</h3>
      </div>
    )}
    {props.type === "manager-small" && (
      <div>
        <img src={MINER_TWO} />
        <h3>{String.NO_DATA}</h3>
        <p>{String.ADD_PARTY}</p>
      </div>
    )}
    {props.type === "tenure" && (
      <div>
        <img src={TENURE} />
        <h3>{String.NO_DATA}</h3>
        <p>{String.ADD_TENURE}</p>
      </div>
    )}
    {props.type === "permit" && (
      <div>
        <img src={PERMIT} />
        <h3>{String.NO_PERMIT}</h3>
      </div>
    )}
    {props.type === "no-results" && (
      <div>
        <img src={NO_MINE} />
        <h3>{String.NO_RESULTS}</h3>
      </div>
    )}
    {props.type === "unauthorized" && (
      <div className="no-nav-bar">
        <img src={NO_MINE} />
        <h3>{String.UNAUTHORIZED}</h3>
        <p>{String.CONTACT_ADMIN}</p>
      </div>
    )}
    {props.type === "view-mine-manager" && (
      <div className="center">
        <img src={GROUP_MINERS} />
        <p>{String.NO_PREV_MINE_MANAGER}</p>
      </div>
    )}
    {props.type === "contacts" && (
      <div>
        <img src={MINER_TWO} />
        <h3>No contacts found</h3>
        <p>Create a contact using the menu above</p>
      </div>
    )}
  </div>
);

NullScreen.propTypes = propTypes;

export default NullScreen;
