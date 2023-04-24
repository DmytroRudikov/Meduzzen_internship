import redis.typing
from typing import List, TextIO
import json
import csv
from app.core.db_config import get_redis_db, get_sql_db
from app.services.crud_quiz import QuizCrud


class ExportRedis:
    def __init__(self):
        self.redis_db = get_redis_db()

    async def get_redis_data(self, redis_keys: redis.typing.KeysT) -> List[dict]:
        redis_values = await self.redis_db.mget(keys=redis_keys)
        results_list = []
        for value in redis_values:
            split_value = value.decode("utf-8").split(";")
            for v in split_value:
                json_dict_results = json.loads(v)
                results_list.append(json_dict_results)
        return results_list

    @staticmethod
    async def write_json_file(results_list: List[dict], outfile: TextIO):
        json.dump(results_list, outfile, indent=4)

    @staticmethod
    async def write_csv_file(fieldnames: List[str], results_list: List[dict], outfile: TextIO):
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_list)

    async def redis_export_json_all_user_results(self, user_id: int) -> TextIO:
        redis_keys = await self.redis_db.keys(f"user_id:{user_id}*")
        results_list = await self.get_redis_data(redis_keys=redis_keys)
        with open(f"app/utils/exported_quiz_results_json/user_{user_id}_all_quizzes_results.json", "w", encoding="utf-8") as outfile:
            await self.write_json_file(results_list=results_list, outfile=outfile)
        return outfile

    async def redis_export_json_all_company_members_results(self, company_id: int) -> TextIO:
        redis_keys = await self.redis_db.keys(f"*company_id:{company_id}*")
        results_list = await self.get_redis_data(redis_keys=redis_keys)
        with open(f"app/utils/exported_quiz_results_json/company_{company_id}_all_members_results.json", "w", encoding="utf-8") as outfile:
            await self.write_json_file(results_list=results_list, outfile=outfile)
        return outfile

    async def redis_export_json_one_company_member_results(self, company_id: int, user_id: int) -> TextIO:
        redis_keys = await self.redis_db.keys(f"user_id:{user_id}:company_id:{company_id}*")
        results_list = await self.get_redis_data(redis_keys=redis_keys)
        with open(f"app/utils/exported_quiz_results_json/company_{company_id}_results_for_member_with_user_id_{user_id}.json", "w", encoding="utf-8") as outfile:
            await self.write_json_file(results_list=results_list, outfile=outfile)
        return outfile

    async def redis_export_json_results_for_one_quiz_in_company(self, company_id: int, quiz_id_in_company: int) -> TextIO:
        redis_keys = await self.redis_db.keys(f"*:company_id:{company_id}:quiz_id_in_company:{quiz_id_in_company}*")
        results_list = await self.get_redis_data(redis_keys=redis_keys)
        with open(f"app/utils/exported_quiz_results_json/company_{company_id}_quiz_id_{quiz_id_in_company}_results.json", "w", encoding="utf-8") as outfile:
            await self.write_json_file(results_list=results_list, outfile=outfile)
        return outfile

    async def redis_export_csv_all_user_results(self, user_id: int) -> TextIO:
        redis_keys = await self.redis_db.keys(f"user_id:{user_id}*")
        results_list = await self.get_redis_data(redis_keys=redis_keys)
        try:
            fieldnames = [key for key in results_list[0]]
        except IndexError:
            fieldnames = []
        with open(f"app/utils/exported_quiz_results_csv/user_{user_id}_all_quizzes_results.csv", "w", newline="", encoding="utf-8") as outfile:
            await self.write_csv_file(fieldnames=fieldnames, results_list=results_list, outfile=outfile)
        return outfile

    async def redis_export_csv_all_company_members_results(self, company_id: int) -> TextIO:
        redis_keys = await self.redis_db.keys(f"*company_id:{company_id}*")
        results_list = await self.get_redis_data(redis_keys=redis_keys)
        try:
            fieldnames = [key for key in results_list[0]]
        except IndexError:
            fieldnames = []
        with open(f"app/utils/exported_quiz_results_csv/company_{company_id}_all_members_results.csv", "w", newline="", encoding="utf-8") as outfile:
            await self.write_csv_file(fieldnames=fieldnames, results_list=results_list, outfile=outfile)
        return outfile

    async def redis_export_csv_one_company_member_results(self, company_id: int, user_id: int) -> TextIO:
        redis_keys = await self.redis_db.keys(f"user_id:{user_id}:company_id:{company_id}*")
        results_list = await self.get_redis_data(redis_keys=redis_keys)
        try:
            fieldnames = [key for key in results_list[0]]
        except IndexError:
            fieldnames = []
        with open(f"app/utils/exported_quiz_results_csv/company_{company_id}_results_for_member_with_user_id_{user_id}.csv", "w", newline="", encoding="utf-8") as outfile:
            await self.write_csv_file(fieldnames=fieldnames, results_list=results_list, outfile=outfile)
        return outfile

    async def redis_export_csv_results_for_one_quiz_in_company(self, company_id: int, quiz_id_in_company: int) -> TextIO:
        redis_keys = await self.redis_db.keys(f"*:company_id:{company_id}:quiz_id_in_company:{quiz_id_in_company}*")
        results_list = await self.get_redis_data(redis_keys=redis_keys)
        try:
            fieldnames = [key for key in results_list[0]]
        except IndexError:
            fieldnames = []
        with open(f"app/utils/exported_quiz_results_csv/company_{company_id}_quiz_id_{quiz_id_in_company}_results.csv", "w", newline="", encoding="utf-8") as outfile:
            await self.write_csv_file(fieldnames=fieldnames, results_list=results_list, outfile=outfile)
        return outfile
