import { IRating } from "@xcpcio/types";
import { generateID, generateName } from "./utils";

const startYear = 2021;
const endYear = 2022;

export const ratingConfig: IRating = {
    id: generateID(startYear, endYear),
    name: generateName(startYear, endYear),
    baseRating: 1900,
    contestIDs: [
        "provincial-contest/2021/zjcpc",
        "provincial-contest/2021/henan",
        "provincial-contest/2021/jilin",
        "provincial-contest/2021/jiangsu",

        "ccpc/7th/guilin",
        "ccpc/7th/guangzhou",
        "ccpc/7th/weihai",
        "ccpc/7th/harbin",
        "ccpc/7th/final",

        "icpc/46th/jinan",
        "icpc/46th/nanjing",
    ],
    users: [],
};
