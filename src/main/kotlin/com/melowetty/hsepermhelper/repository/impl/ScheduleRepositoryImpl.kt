package com.melowetty.hsepermhelper.repository.impl

import Lesson
import LessonType
import Schedule
import com.melowetty.hsepermhelper.exceptions.ScheduleNotFoundException
import com.melowetty.hsepermhelper.repository.ScheduleRepository
import com.melowetty.hsepermhelper.utils.getHash
import org.apache.poi.ss.usermodel.*
import org.springframework.stereotype.Component
import java.io.File
import java.io.FileNotFoundException
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.LocalTime
import java.time.format.DateTimeFormatter

@Component
class ScheduleRepositoryImpl: ScheduleRepository {
    private var currentSchedule: Schedule? = null
    private var nextSchedule: Schedule? = null

    override fun getCurrentSchedule(): Schedule? {
        if(currentSchedule == null) return retrieveCurrentSchedule()
        val currentTime = LocalDateTime.now()
        val differentMinutes = (currentTime.minute - currentSchedule?.parsedDate?.minute!!)
        if(differentMinutes > 5) return retrieveCurrentSchedule()
        return currentSchedule
    }

    override fun getNextSchedule(): Schedule? {
        if(nextSchedule == null) return retrieveNextSchedule()
        val currentTime = LocalDateTime.now()
        val differentMinutes = (currentTime.minute - nextSchedule?.parsedDate?.minute!!)
        if(differentMinutes > 5) return retrieveNextSchedule()
        return nextSchedule
    }

    override fun getAvailableCourses(): List<Int> {
        if(getCurrentSchedule() == null) throw ScheduleNotFoundException("Расписание не найдено!")
        val courses = currentSchedule!!.lessons.values.flatMap { lessons ->
            lessons.map { it.course }
        }.toSortedSet().toList()
        if(courses.isEmpty()) throw RuntimeException("Возникли проблемы с обработкой расписания!")
        return courses
    }

    override fun getAvailablePrograms(course: Int): List<String> {
        if (getCurrentSchedule() == null) throw ScheduleNotFoundException("Расписание не найдено!")
        val programs = currentSchedule!!.lessons.values
            .asSequence()
            .flatten()
            .filter { it.course == course }
            .map { it.programme }
            .toSortedSet()
            .toList()
        if(programs.isEmpty()) throw IllegalArgumentException("Курс не найден в расписании!")
        return programs
    }

    override fun getAvailableGroups(course: Int, program: String): List<String> {
        if (getCurrentSchedule() == null) throw ScheduleNotFoundException("Расписание не найдено!")
        val groups = currentSchedule!!.lessons.values
            .asSequence()
            .flatten()
            .filter { it.course == course && it.programme == program }
            .map { it.group }
            .toSortedSet()
            .toList()
        if(groups.isEmpty()) throw IllegalArgumentException("Программа не найдена в расписании!")
        return groups
    }

    override fun getAvailableSubgroups(course: Int, program: String, group: String): List<Int> {
        if (getCurrentSchedule() == null) throw ScheduleNotFoundException("Расписание не найдено!")
        val groups = getAvailableGroups(course, program)
        if(groups.isEmpty()) throw IllegalArgumentException("Группа не найдена в расписании!")
        val groupNumRegex = Regex("[А-Яа-яЁёa-zA-Z]+-\\d*-(\\d*)")
        try {
            val matches = groupNumRegex.find(groups.last())
            val lastGroupNumMatch = matches!!.groups[1]
            val lastGroupNum = lastGroupNumMatch!!.value.toInt()
            return (1..lastGroupNum * 2).toList()
        } catch (e: Exception) {
            throw RuntimeException("Возникли проблемы с обработкой группы!")
        }
    }

    private fun getFile(path: String): File {
        try {
            val file = File(path)
            if (!file.isFile) throw ScheduleNotFoundException("Файл с расписанием не найден!")
            return file
        } catch (exception: FileNotFoundException) {
            throw ScheduleNotFoundException("Файл с расписанием не найден!")
        }
    }

    private fun retrieveCurrentSchedule(): Schedule? {
        val file = getFile(CURRENT_SCHEDULE_FILE)
        currentSchedule = parseSchedule(file)
        return currentSchedule
    }

    private fun retrieveNextSchedule(): Schedule? {
        val file = getFile(NEXT_SCHEDULE_FILE)
        nextSchedule = parseSchedule(file)
        return nextSchedule
    }

    private fun getWorkbook(file: File): Workbook {
        return WorkbookFactory.create(file)
    }

    private fun getProgramme(programme: String): String {
        val programmeRegex = Regex("[А-Яа-яЁёa-zA-Z]+")
        return programmeRegex.find(programme)?.value ?: ""
    }

    private fun getCourse(sheetName: String): Int {
        val courseRegex = Regex(pattern = "[0-9]+")
        return (courseRegex.find(sheetName)?.value ?: "0").toInt()
    }

    private fun parseSchedule(file: File): Schedule? {
        try {
            val hash = getHash(file)
            val workbook = getWorkbook(file)
            val lessonsList = mutableListOf<Lesson>()
            val (weekNum, weekStart, weekEnd) = getWeekInfo(getValue(
                workbook.getSheetAt(1),
                workbook.getSheetAt(1).getRow(1).getCell(3))
            )
            if (weekStart == null || weekEnd == null) {
                return null
            }
            var isSession = false
            if(weekNum == null) {
                isSession = true
            }
            for (i in 0 until workbook.numberOfSheets) {
                val sheet = workbook.getSheetAt(i)
                if (sheet.sheetName.lowercase() == "доц") continue
                val course = getCourse(sheet.sheetName)
                val groups = mutableMapOf<Int, String>()
                val programs = mutableMapOf<Int, String>()
                for (cellNum in 2 until sheet.getRow(2).physicalNumberOfCells) {
                    val group = getValue(sheet, sheet.getRow(2).getCell(cellNum))
                    if (group != "") {
                        groups[cellNum] = group
                        val programme = getProgramme(group)
                        programs[cellNum] = programme
                    }
                }
                run schedule@ {
                    for(rowNum in 3 until sheet.lastRowNum) {
                        val row = sheet.getRow(rowNum)
                        val unparsedDate = getValue(sheet, row.getCell(0)).split("\n")
                        if (unparsedDate.size < 2) break
                        val date = LocalDate.parse(unparsedDate[1], DateTimeFormatter.ofPattern("dd.MM.yyyy"))
                        val time = getValue(sheet, row.getCell(1)).split("\n")[2]
                        val timeRegex = Regex("[0-9]+:[0-9]+")
                        val timeRegexMatches = timeRegex.findAll(time)
                        val startTime = timeRegexMatches.elementAt(0).value
                        val splitStartTime = startTime.split(":")
                        val startLocalTime = LocalTime.of(splitStartTime[0].toInt(), splitStartTime[1].toInt())
                        val startLocalDateTime = LocalDateTime.of(date, startLocalTime)
                        val endTime = timeRegexMatches.elementAt(1).value
                        val splitEndTime = endTime.split(":")
                        val endLocalTime = LocalTime.of(splitEndTime[0].toInt(), splitEndTime[1].toInt())
                        val endLocalDateTime = LocalDateTime.of(date, endLocalTime)
                        run line@ {
                            for (cellNum in 2 until row.physicalNumberOfCells) {
                                val cell = row.getCell(cellNum)
                                val group = groups.getOrDefault(cellNum, "")
                                if (group == "") {
                                    return@line
                                }
                                val programme = programs.getOrDefault(cellNum, "N/a")
                                val font = workbook.getFontAt(cell.cellStyle.fontIndex)
                                val isUnderlined = font.underline != Font.U_NONE
                                val lessons = getLesson(
                                    course = course,
                                    programme = programme,
                                    group = group,
                                    date = date,
                                    startTimeStr = startTime,
                                    endTimeStr = endTime,
                                    startTime = startLocalDateTime,
                                    endTime = endLocalDateTime,
                                    isUnderlined = isUnderlined,
                                    cellValue = getValue(sheet = sheet, cell = cell)
                                )
                                for (lesson in lessons) {
                                    lessonsList.add(lesson)
                                }
                            }
                        }
                    }
                }
            }
            return Schedule(
                weekNumber = weekNum,
                weekStart = weekStart,
                weekEnd = weekEnd,
                lessons = lessonsList.groupBy {
                    it.date
                },
                isSession = isSession,
                parsedDate = LocalDateTime.now(),
                hash = hash,
            )
        } catch (exception: Exception) {
            throw RuntimeException("Произошла ошибка во время обработки файла с расписанием!")
        }
    }

    private fun getValue(sheet: Sheet, cell: Cell?): String {
        if (cell == null) return ""
        for(region in sheet.mergedRegions){
            if(region.isInRange(cell)) {
                return sheet.getRow(region.firstRow).getCell(region.firstColumn).stringCellValue
            }
        }
        return cell.stringCellValue ?: ""
    }

    private fun getLesson(
        course: Int,
        programme: String,
        group: String,
        date: LocalDate,
        startTimeStr: String,
        endTimeStr: String,
        startTime: LocalDateTime,
        endTime: LocalDateTime,
        isUnderlined: Boolean,
        cellValue: String
    ): List<Lesson> {
        val splitCell = cellValue.split("\n").toMutableList()
        splitCell.removeAll(listOf(""))
        if(splitCell.size == 3) {
            val lessons = mutableListOf<Lesson>()
            lessons.add(
                parseLesson(
                    course = course,
                    programme = programme,
                    group = group,
                    date = date,
                    startTimeStr = startTimeStr,
                    endTimeStr = endTimeStr,
                    startTime = startTime,
                    endTime = endTime,
                    isUnderlined = isUnderlined,
                    splitCell.subList(0, 2)
                )
            )
            val newCell = splitCell.toMutableList()
            newCell.removeAt(1)
            lessons.add(
                parseLesson(
                    course = course,
                    programme = programme,
                    group = group,
                    date = date,
                    startTimeStr = startTimeStr,
                    endTimeStr = endTimeStr,
                    startTime = startTime,
                    endTime = endTime,
                    isUnderlined = isUnderlined,
                    newCell
                )
            )
        }
        else if(splitCell.size % 2 == 0) {
            val lessons = mutableListOf<Lesson>()
            for (i in 0 until splitCell.size / 2) {
                lessons.add(
                    parseLesson(
                        course = course,
                        programme = programme,
                        group = group,
                        date = date,
                        startTimeStr = startTimeStr,
                        endTimeStr = endTimeStr,
                        startTime = startTime,
                        endTime = endTime,
                        isUnderlined = isUnderlined,
                        splitCell.subList(i * 2, (i + 1) * 2)
                    )
                )
            }
            return lessons
        }
        return listOf(
            parseLesson(
                course = course,
                programme = programme,
                group = group,
                date = date,
                startTimeStr = startTimeStr,
                endTimeStr = endTimeStr,
                startTime = startTime,
                endTime = endTime,
                isUnderlined = isUnderlined,
                line = splitCell[0]
            )
        )
    }

    private fun parseLesson(
        course: Int,
        programme: String,
        group: String,
        date: LocalDate,
        startTimeStr: String,
        endTimeStr: String,
        startTime: LocalDateTime,
        endTime: LocalDateTime,
        isUnderlined: Boolean,
        line: String
    ): Lesson {
        val subject = line
        val lessonType = getLessonType(
            subject = subject,
            isUnderlined = isUnderlined
        )
        return Lesson(
            subject = subject,
            course = course,
            programme = programme,
            group = group,
            subGroup = null,
            date = date,
            startTimeStr = startTimeStr,
            endTimeStr = endTimeStr,
            startTime = startTime,
            endTime = endTime,
            lecturer = null,
            office = null,
            building = null,
            lessonType = lessonType,
        )
    }

    private fun parseLesson(
        course: Int,
        programme: String,
        group: String,
        date: LocalDate,
        startTimeStr: String,
        endTimeStr: String,
        startTime: LocalDateTime,
        endTime: LocalDateTime,
        isUnderlined: Boolean,
        lines: List<String>,
    ): Lesson {
        val subject = lines[0].strip()
        val lessonInfo = lines[1].strip()
        val lessonInfoRegex = Regex("([^\\/]*)\\((.*)\\)")
        val lessonInfoMatch = lessonInfoRegex.find(lessonInfo)
        val lessonInfoGroups = lessonInfoMatch?.groups
        val lecturer = getLecturer(lessonInfoGroups?.get(1)?.value?.strip())
        val info = lessonInfoGroups?.get(2)?.value
        val infoRegex = Regex("([^\\[\\]\\,]+)")
        val infoMatches = info?.let { infoRegex.findAll(it) }
        val office = infoMatches?.elementAt(0)?.groups?.get(1)?.value?.strip()
        val building = (infoMatches?.elementAt(1)?.groups?.get(1)?.value)?.toIntOrNull()
        val subGroup = (getSubGroup(infoMatches)?.strip())?.toIntOrNull()
        val lessonType = getLessonType(
            subject = subject,
            lessonInfo = lecturer,
            isUnderlined = isUnderlined
        )
        return Lesson(
            subject = subject,
            course = course,
            programme = programme,
            group = group,
            subGroup = subGroup,
            date = date,
            startTimeStr = startTimeStr,
            endTimeStr = endTimeStr,
            startTime = startTime,
            endTime = endTime,
            lecturer = lecturer,
            office = office,
            building = building,
            lessonType = lessonType,
        )
    }

    fun getSubGroup(matchResult: Sequence<MatchResult>?): String? {
        if (matchResult == null) return null
        if (matchResult.count() < 3) {
            return null
        }
        return matchResult.elementAt(2).groups.get(1)?.value
    }

    private fun getLessonType(
        subject: String,
        lessonInfo: String? = "",
        isUnderlined: Boolean,
    ): LessonType {
        val pureSubject = subject.lowercase()
        val pureLessonInfo = lessonInfo?.lowercase()
        if (pureSubject.contains("(ведомост")) return LessonType.STATEMENT
        if (pureSubject.contains("экзамен")
            || pureSubject.contains("зачёт")
            || pureSubject.contains("зачет")
            ) return LessonType.EXAM
        if (pureSubject.contains("английский язык")) return LessonType.ENGLISH
        if (pureSubject.contains("майнор")) return LessonType.MINOR
        if (pureSubject == "практика") return LessonType.PRACTICE
        if (pureLessonInfo?.contains("мкд") == true) return LessonType.ICC
        if (pureSubject.contains("лекция") || pureSubject.contains("лекции")) return LessonType.LECTURE
        if (pureSubject.contains("семинар") || pureSubject.contains("семинары")) return LessonType.SEMINAR
        if (isUnderlined) return LessonType.LECTURE
        return LessonType.SEMINAR
    }

    private fun getWeekInfo(weekInfoStr: String): Triple<Int?, LocalDate?, LocalDate?> {
        val weekInfoRegex = Regex("\\D*(\\d*).+\\s+(\\d+\\.\\d+\\.\\d+)\\s.+\\s(\\d+\\.\\d+\\.\\d+)")
        val weekInfoMatches = weekInfoRegex.findAll(weekInfoStr)
        val weekInfoGroups = weekInfoMatches.elementAt(0).groups
        val weekNumber = (weekInfoGroups.get(1)?.value?.strip())?.toIntOrNull()
        val datePattern = DateTimeFormatter.ofPattern("dd.MM.yyyy")
        val weekStart = LocalDate.parse(weekInfoGroups.get(2)?.value, datePattern)
        val weekEnd = LocalDate.parse(weekInfoGroups.get(3)?.value, datePattern)
        return Triple(weekNumber, weekStart, weekEnd)
    }

    private fun getLecturer(str: String?): String? {
        if (str == null) return null
        if (str.isEmpty()) return null
        return str
    }

    companion object {
        const val CURRENT_SCHEDULE_FILE = "rasp2.xls"
        const val NEXT_SCHEDULE_FILE = "rasp.xls"
    }
}