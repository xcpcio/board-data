import type { IRating } from "@xcpcio/types";
import { generateID, generateName } from "./utils";

const startYear = 2020;
const endYear = 2021;

export const ratingConfig: IRating = {
  id: generateID(startYear, endYear),
  name: generateName(startYear, endYear),
  baseRating: 1900,
  contestIDs: [
    "provincial-contest/2020/zjcpc",
    "provincial-contest/2020/henancpc",

    "ccpc/2020/qinhuangdao",
    "ccpc/2020/weihai",
    "ccpc/2020/mianyang",
    "ccpc/2020/changchun",
    "ccpc/2020/final",

    "icpc/2020/shanghai",
    "icpc/2020/nanjing",
    "icpc/2020/jinan",
    "icpc/2020/kunming",
    "icpc/2020/shenyang",
  ],
  users: [],
};
