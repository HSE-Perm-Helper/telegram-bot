import com.fasterxml.jackson.annotation.JsonFormat
import com.fasterxml.jackson.annotation.JsonIgnore
import com.fasterxml.jackson.annotation.JsonProperty
import com.melowetty.hsepermhelper.utils.DateUtils
import java.time.LocalDate
import java.time.LocalDateTime

data class Lesson(
    val subject: String,
    @JsonIgnore val course: Int,
    @JsonIgnore val programme: String,
    @JsonIgnore val group: String,
    @JsonIgnore val subGroup: Int?,
    @JsonFormat(pattern = DateUtils.DATE_PATTERN)
    val date: LocalDate,
    @JsonProperty("startTime") val startTimeStr: String,
    @JsonProperty("endTime") val endTimeStr: String,
    @JsonIgnore val startTime: LocalDateTime,
    @JsonIgnore val endTime: LocalDateTime,
    val lecturer: String?,
    val office: String?,
    val building: Int?,
    val lessonType: LessonType,
)
