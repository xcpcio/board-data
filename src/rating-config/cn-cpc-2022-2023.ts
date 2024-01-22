import { IRating } from "@xcpcio/types";
import { generateID, generateName } from "./utils";

const startYear = 2022;
const endYear = 2023;

export const ratingConfig: IRating = {
    id: generateID(startYear, endYear),
    name: generateName(startYear, endYear),
    baseRating: 1900,
    contestIDs: [
        "provincial-contest/2022/zjcpc",
        "provincial-contest/2022/hbcpc",
        "provincial-contest/2022/jiangsu",
        "provincial-contest/2022/guangdong",

        "ccpc/8th/guilin",
        "ccpc/8th/weihai",
        "ccpc/8th/guangzhou",
        "ccpc/8th/mianyang",
        "ccpc/8th/final",

        "icpc/47th/shenyang",
        "icpc/47th/xian",
        "icpc/47th/hefei",
        "icpc/47th/jinan",
        "icpc/47th/hangzhou",
        "icpc/47th/nanjing",
    ],
    users: [],
};
