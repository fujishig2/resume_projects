
def attributeClosureInterface(pass_connection, pass_cursor):
        global cursor, connection
        connection=pass_connection
        cursor=pass_cursor
        while True:

                # get schema names
                schemaString = input("\nEnter the schemas that contain the funcitonal dependencies separated by commas or q to go back to previous menu:\n==>")
                if schemaString.strip().lower() == 'q':
                        return

                # get all valid schemas
                cmd = """
                SELECT Name
                FROM InputRelationSchemas;
                """
                cursor.execute(cmd)
                rows = cursor.fetchall()
                validSchemas = [row["Name"] for row in rows]

                # validate schema inputs
                valid = True
                schemaList = schemaString.strip().split(',')
                for i in range(len(schemaList)):
                        schemaList[i] = schemaList[i].strip()
                        if schemaList[i] not in validSchemas:
                                valid = False
                                break
                if not valid:
                        print("\n***Invalid schema names***")
                        continue

                # get attributes
                attInput = input("Enter attributes separated by commas q to go back to previous menu:\n==>")
                if attInput.strip().lower() == 'q':
                        return

                # put attributes into a set
                attSet = set()
                attList = attInput.strip().split(',')
                for att in attList:
                        att = att.strip()
                        attSet.add(att)

                # validate attributes
                validAttributes = set()
                for schema in schemaList:
                        cmd = """
                        SELECT Attributes
                        FROM InputRelationSchemas
                        WHERE Name = ? """
                        cursor.execute(cmd,(schema,))
                        attString = cursor.fetchone()[0]
                        attList = attString.strip().split(',')
                        validAttributes |= set(attList)
                if not (attSet <= validAttributes):
                        print("***Invalid attributes***")
                        continue

                # get functional dependencies from the specified schemas
                fdList = []
                for schema in schemaList:
                        schema = schema.strip()

                        # get fds from the schema
                        cmd = """
                        SELECT FDs
                        FROM InputRelationSchemas
                        WHERE Name = ?
                        """
                        cursor.execute(cmd, (schema,))
                        row = cursor.fetchone()
                        fds = row['FDs'].split(';')
                        for fdstring in fds:
                                fdstring = fdstring.strip().split('=>')
                                lhs = set(fdstring[0].strip('{').strip('}').split(','))
                                rhs = set(fdstring[1].strip('{').strip('}').split(','))
                                fd = (lhs, rhs)
                                if fd not in fdList:
                                        fdList.append(fd)




                # compute attribute closure in respect to fdList
                closure = list(attribute_closure_single(fdList, attSet))

                # print output
                closure.sort()
                closureString = "{"
                for i in range(len(closure)):
                        if i == (len(closure) - 1):
                                closureString = closureString + str(closure[i])
                        else:
                                closureString = closureString + str(closure[i]) + ', '
                closureString += "}"
                print("Result")
                print("-------")
                print(closureString, "\n")

        return

def attribute_closure_single(fds, attribute):
        old={}
        closure=attribute
        while old != closure:
                old = closure
                for fd in fds:
                        if fd[0] <= closure and fd[1] not in closure:
                                closure = closure.union(fd[1])
        return closure


def main():
        import sqlite3
        global db, cursor
        db = sqlite3.connect('./example.db')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        db.execute('PRAGMA foreign_keys=ON;')
        db.commit()

        attributeClosureInterface()

if __name__ == "__main__":
        main()
