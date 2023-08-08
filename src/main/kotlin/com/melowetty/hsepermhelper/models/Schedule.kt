import com.fasterxml.jackson.annotation.JsonFormat
import com.fasterxml.jackson.annotation.JsonGetter
import com.fasterxml.jackson.annotation.JsonIgnore
import com.melowetty.hsepermhelper.utils.DateUtils
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

data class Schedule(
    val weekNumber: Int?,
    val lessons: Map<LocalDate, List<Lesson>>,
    @JsonFormat(pattern = DateUtils.DATE_PATTERN)
    val weekStart: LocalDate,
    @JsonFormat(pattern = DateUtils.DATE_PATTERN)
    val weekEnd: LocalDate,
    val isSession: Boolean = false,
    @JsonIgnore val parsedDate: LocalDateTime,
    @JsonIgnore val hash: String,
) {
    @JsonGetter("lessons")
    fun getFormattedLessons(): Set<Map.Entry<String, List<Lesson>>> {
        return lessons.mapKeys { it.key.format(DateTimeFormatter.ofPattern(DateUtils.DATE_PATTERN)) }.entries
    }
}
