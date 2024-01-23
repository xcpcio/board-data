import type { IRating } from "@xcpcio/types";
import { generateID, generateName } from "./utils";

const startYear = 2023;
const endYear = 2024;

export const ratingConfig: IRating = {
  id: generateID(startYear, endYear),
  name: generateName(startYear, endYear),
  baseRating: 1900,
  contestIDs: [
    "provincial-contest/2023/zhejiang",
    "provincial-contest/2023/guangdong",
    "provincial-contest/2023/hunan",
    "provincial-contest/2023/henan",

    "ccpc/9th/qinhuangdao",
    "ccpc/9th/guilin",
    "ccpc/9th/harbin",
    "ccpc/9th/shenzhen",

    "icpc/48th/shenyang",
    "icpc/48th/nanjing",
    "icpc/48th/hefei",
    "icpc/48th/jinan",
    "icpc/48th/hangzhou",
    "icpc/48th/ecfinal",
  ],
  users: [],
};
