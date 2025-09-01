import dayjs from "dayjs";
import LocalizedFormat from "dayjs/plugin/localizedFormat";
import RelativeTime from "dayjs/plugin/relativeTime";
import "dayjs/locale/en";

dayjs.extend(LocalizedFormat);
dayjs.extend(RelativeTime);
dayjs.locale("en");

export default dayjs;
